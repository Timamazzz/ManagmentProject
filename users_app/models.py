from calendar import monthrange
from datetime import date

import openpyxl
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField
from django.db import transaction


# Create your models here.
class User(AbstractUser):
    pass


class Volunteer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('dismissed', 'Уволен'),
        ('reserve', 'Резерв'),
    ]
    number_service = models.IntegerField(verbose_name="Номер табельный")

    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=30, blank=True, null=True, verbose_name="Отчество")

    birthday = models.DateField(verbose_name="Дата рождения")

    passport_series = models.CharField(max_length=10, verbose_name="Серия паспорта")
    passport_number = models.CharField(max_length=15, verbose_name="Номер паспорта")
    passport_issued = models.CharField(max_length=255, verbose_name="Кем выдан паспорт")
    passport_issue_date = models.DateField(verbose_name="Дата выдачи паспорта")

    contract_date = models.DateField(verbose_name="Дата заключения контракта")
    order_number = models.CharField(max_length=50, verbose_name="Номер приказа")
    enrollment_date = models.DateField(verbose_name="Дата зачисления в добровольческое формирование")

    salary_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Размер денежной выплаты")

    bic = models.CharField(max_length=9, verbose_name="БИК")
    bank_name = models.CharField(max_length=255, verbose_name="Наименование кредитной организации")
    correspondent_account = models.CharField(max_length=20, verbose_name="Корреспондентский счет")
    checking_account = models.CharField(max_length=20, verbose_name="Расчетный счет")
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    kpp = models.CharField(max_length=9, verbose_name="КПП")

    dismissal_date = models.DateField(blank=True, null=True, verbose_name="Дата увольнения")
    dismissal_order_number = models.CharField(max_length=50, blank=True, null=True,
                                              verbose_name="Номер приказа об увольнении")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Статус")

    class Meta:
        verbose_name = "Доброволец"
        verbose_name_plural = "Добровольцы"
        permissions = [
            ("can_manage_reserve", "Может управлять резервистами"),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.number_service})"

    def clean(self):
        """Пользовательская валидация для добровольца"""
        if self.status == 'dismissed':
            if not self.dismissal_date:
                raise ValidationError({
                    'dismissal_date': _("При увольнении необходимо указать дату увольнения!")
                })
            if not self.dismissal_order_number:
                raise ValidationError({
                    'dismissal_order_number': _("При увольнении необходимо указать номер приказа!")
                })
            if self.dismissal_date and self.enrollment_date and self.dismissal_date < self.enrollment_date:
                raise ValidationError({
                    'dismissal_date': _("Дата увольнения не может быть раньше даты зачисления!")
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Remark(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name="remarks",
                                  verbose_name="Доброволец")
    date = models.DateField(verbose_name="Дата нарекания")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий к нареканию")

    class Meta:
        verbose_name = "Нарекание"
        verbose_name_plural = "Нарекания"

    def __str__(self):
        return f"Нарекание {self.volunteer.last_name} {self.volunteer.first_name} ({self.date})"


class Item(models.Model):
    CHARACTERISTICS_SCHEMA = {
        'type': 'list',
        'items': {
            'type': 'dict',
            'keys': {
                'name': {
                    'type': 'string',
                    'title': 'Название'
                },
                'value': {
                    'type': 'string',
                    'title': 'Значение'
                }
            }
        }
    }
    """Модель для предметов с характеристиками"""
    name = models.CharField(max_length=255, verbose_name="Название предмета")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    characteristics = JSONField(blank=True, null=True, verbose_name='Характеристики', schema=CHARACTERISTICS_SCHEMA)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class VolunteerItem(models.Model):
    """Связь между добровольцем и предметами"""
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name="items", verbose_name="Доброволец")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="volunteers", verbose_name="Предмет")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Предмет для добровольца"
        verbose_name_plural = "Предметы для добровольцев"
        unique_together = (
            'volunteer',
            'item')

    def __str__(self):
        return f"{self.volunteer} - {self.item.name} (Кол-во: {self.quantity})"


class Report(models.Model):
    """Отчет за период"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания отчета")
    file = models.FileField(upload_to="reports/", blank=True, null=True, verbose_name="Файл отчета")
    year = models.IntegerField(verbose_name="Год", default=date.today().year)
    month = models.IntegerField(verbose_name="Месяц", choices=[(i, month) for i, month in enumerate([
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ], start=1)], default=date.today().month)

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        start_date = self.get_start_date()
        end_date = self.get_end_date()
        return f"Отчет с {start_date} по {end_date}"

    def get_start_date(self):
        """Получение начала месяца"""
        return date(self.year, self.month, 1)

    def get_end_date(self):
        """Получение конца месяца"""
        last_day = monthrange(self.year, self.month)[1]
        return date(self.year, self.month, last_day)

    def get_volunteers_for_report(self):
        """Фильтрация добровольцев для отчета"""
        start_date = self.get_start_date()
        end_date = self.get_end_date()
        return Volunteer.objects.filter(
            enrollment_date__lte=end_date,
            dismissal_date__isnull=True
        ).exclude(
            remarks__date__range=(start_date, end_date)
        )

    def generate_report(self):
        """Создание Excel-файла отчета"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Отчет"

        headers = [
            "id", "№ табельный", "Статус", "Фамилия", "Имя", "Отчество",
            "Дата рождения", "Серия паспорта", "Номер паспорта", "Кем выдан паспорт",
            "Дата выдачи паспорта", "Дата контракта", "№ приказа", "Дата зачисления",
            "Размер денежной выплаты", "БИК", "Банк", "Корр. счет", "Расчетный счет", "ИНН", "КПП"
        ]
        ws.append(headers)

        for volunteer in self.get_volunteers_for_report():
            row = [
                volunteer.id, volunteer.number_service, volunteer.get_status_display(),
                volunteer.last_name, volunteer.first_name, volunteer.patronymic,
                volunteer.birthday, volunteer.passport_series, volunteer.passport_number, volunteer.passport_issued,
                volunteer.passport_issue_date, volunteer.contract_date, volunteer.order_number,
                volunteer.enrollment_date, volunteer.salary_amount, volunteer.bic, volunteer.bank_name,
                volunteer.correspondent_account, volunteer.checking_account, volunteer.inn, volunteer.kpp
            ]
            ws.append(row)

        file_stream = ContentFile(b"")
        wb.save(file_stream)
        file_stream.seek(0)
        filename = f"report_{self.year}_{self.month}.xlsx"
        self.file.save(filename, file_stream, save=False)

    def save(self, *args, **kwargs):
        self.generate_report()
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self.__str__()

    name.fget.short_description = 'Название'


class ActivityReport(models.Model):
    """Отчет активности добровольцев"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания отчета")
    report_date = models.DateField(verbose_name="Дата активности")
    file = models.FileField(upload_to="activity_reports/", verbose_name="Файл отчета")

    class Meta:
        verbose_name = "Отчет активности"
        verbose_name_plural = "Отчеты активности"

    def __str__(self):
        return f"Отчет активности ({self.report_date.strftime('%Y-%m-%d')})"

    def clean(self):
        """Валидация: файл и дата обязательны"""
        if not self.file:
            raise ValidationError({"file": _("Необходимо загрузить файл отчета.")})
        if not self.report_date:
            raise ValidationError({"report_date": _("Необходимо указать дату активности.")})

    def process_report(self):
        """Обработка загруженного файла и увольнение отсутствующих добровольцев"""
        with transaction.atomic():
            wb = openpyxl.load_workbook(self.file)
            ws = wb.active

            # Поиск столбца с табельными номерами
            header_row = [str(cell).strip().lower() for cell in
                          next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
            tn_keywords = {"тн", "табельный номер"}
            tn_col_index = None

            for idx, header in enumerate(header_row):
                if any(keyword in header for keyword in tn_keywords):
                    tn_col_index = idx
                    break

            if tn_col_index is None:
                raise ValueError("Не найден столбец с табельными номерами")

            report_tn = set()
            for row in ws.iter_rows(min_row=2, values_only=True):
                tn = row[tn_col_index]
                if isinstance(tn, int):
                    report_tn.add(tn)

            active_volunteers = Volunteer.objects.filter(status='active')
            for volunteer in active_volunteers:
                if volunteer.number_service not in report_tn:
                    volunteer.status = 'dismissed'
                    volunteer.dismissal_date = self.report_date
                    volunteer.dismissal_order_number = f"Автоувольнение {self.report_date}"
                    volunteer.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.process_report()
