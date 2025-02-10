import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from users_app.models import Volunteer, Item, VolunteerItem


FIRST_NAMES = ["Иван", "Петр", "Алексей", "Сергей", "Михаил", "Дмитрий", "Егор", "Николай", "Андрей", "Владимир"]
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Смирнов", "Козлов", "Воробьев", "Семенов", "Морозов", "Федоров",
              "Михайлов"]
PATRONYMICS = ["Иванович", "Петрович", "Алексеевич", "Сергеевич", "Михайлович", "Дмитриевич", "Егорович", "Николаевич"]

ITEM_NAMES = ["Рюкзак", "Ковка", "Шлем", "Перчатки", "Турка", "Книга", "Термос", "Лопата", "Комплект", "Нож"]
ITEM_DESCRIPTIONS = ["Описание предмета", "Предмет для выполнения работы", "Снаряжение для похода", "Удобная вещь для активного отдыха"]

class Command(BaseCommand):
    help = "Создает тестовые данные для модели Volunteer и других моделей с связями"

    def handle(self, *args, **kwargs):
        # Очистка базы данных (кроме пользователей)
        Volunteer.objects.all().delete()
        Item.objects.all().delete()
        VolunteerItem.objects.all().delete()

        # Генерация предметов
        items = []
        for i in range(50):  # Генерация 50 предметов
            name = random.choice(ITEM_NAMES)
            description = random.choice(ITEM_DESCRIPTIONS)
            item = Item(
                name=name,
                description=description,
                characteristics=[]  # Пусть характеристики пока будут пустыми
            )
            items.append(item)
        Item.objects.bulk_create(items)

        # Генерация волонтеров
        volunteers = []
        for i in range(100):  # Генерация 100 добровольцев
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            patronymic = random.choice(PATRONYMICS)

            birthday = datetime.today() - timedelta(days=random.randint(7000, 20000))  # Возраст от 20 до 55 лет
            passport_series = f"{random.randint(10, 99)}{random.randint(10, 99)}"
            passport_number = f"{random.randint(100000, 999999)}"
            passport_issued = f"Отдел МВД г. {last_name}ск"
            passport_issue_date = birthday + timedelta(days=random.randint(6000, 10000))

            contract_date = datetime.today() - timedelta(days=random.randint(30, 365))
            order_number = f"{random.randint(100, 999)}-Д"
            enrollment_date = contract_date + timedelta(days=random.randint(1, 10))

            salary_amount = round(random.uniform(30000, 80000), 2)

            bic = f"{random.randint(100000000, 999999999)}"
            bank_name = "ПАО 'ТестБанк'"
            correspondent_account = f"{random.randint(10000000000000000000, 99999999999999999999)}"
            checking_account = f"{random.randint(10000000000000000000, 99999999999999999999)}"
            inn = f"{random.randint(100000000000, 999999999999)}"
            kpp = f"{random.randint(100000000, 999999999)}"

            status = random.choice(['active', 'dismissed'])  # Статус случайным образом

            dismissal_date = None
            dismissal_order_number = None
            if status == 'dismissed':
                dismissal_date = datetime.today() - timedelta(days=random.randint(1, 365))
                dismissal_order_number = f"{random.randint(100, 999)}-У"

            volunteer = Volunteer(
                number_service=random.randint(10000, 99999),
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
                birthday=birthday.date(),
                passport_series=passport_series,
                passport_number=passport_number,
                passport_issued=passport_issued,
                passport_issue_date=passport_issue_date.date(),
                contract_date=contract_date.date(),
                order_number=order_number,
                enrollment_date=enrollment_date.date(),
                salary_amount=salary_amount,
                bic=bic,
                bank_name=bank_name,
                correspondent_account=correspondent_account,
                checking_account=checking_account,
                inn=inn,
                kpp=kpp,
                status=status,
                dismissal_date=dismissal_date,
                dismissal_order_number=dismissal_order_number
            )
            volunteers.append(volunteer)

        Volunteer.objects.bulk_create(volunteers)

        # Генерация связей между волонтерами и предметами
        volunteer_items = []
        for volunteer in volunteers:
            # Генерируем случайное количество предметов для каждого добровольца
            num_items = random.randint(1, 5)  # от 1 до 5 предметов для одного волонтера
            volunteer_items_for_volunteer = random.sample(items, num_items)  # случайные предметы
            for item in volunteer_items_for_volunteer:
                quantity = random.randint(1, 3)  # Количество предмета для волонтера
                volunteer_item = VolunteerItem(
                    volunteer=volunteer,
                    item=item,
                    quantity=quantity
                )
                volunteer_items.append(volunteer_item)

        VolunteerItem.objects.bulk_create(volunteer_items)

        self.stdout.write(self.style.SUCCESS(f"✅ Успешно создано {len(volunteers)} тестовых добровольцев и {len(items)} предметов с связями!"))
