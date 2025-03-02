import random
import openpyxl
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from pathlib import Path


class Command(BaseCommand):
    help = "Генерирует файл отчета активности добровольцев с точной структурой исходного образца"

    HEADERS = [
        "№ п/п", "№ по штату, (для назначения)", "Табельный номер", "Воинская должность", "Номер отряда",
        "Штатная категория", "Воинское звание", "Дата присвоения", "Кем присвоено", "Номер приказа о присвоении",
        # Добавить остальные 77 заголовков
    ]

    def add_arguments(self, parser):
        parser.add_argument("--n", type=int, default=5000, help="Количество записей (по умолчанию 5000)")

    def handle(self, *args, **options):
        n = options["n"]
        file_name = f"activity_report_{now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        file_path = Path("activity_reports") / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Отчет активности"

        # Заголовки
        ws.append(self.HEADERS)

        # Генерация данных
        for i in range(n):
            row_data = [
                i + 1,  # № п/п
                random.randint(1000, 9999),  # № по штату
                100000 + i,  # Табельный номер
                f"Должность{i}",  # Воинская должность
                random.randint(1, 20),  # Номер отряда
                f"Категория{i}",  # Штатная категория
                f"Звание{i}",  # Воинское звание
                f"{random.randint(1950, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                # Дата присвоения
                f"Командир{i}",  # Кем присвоено
                f"Приказ-{i}",  # Номер приказа о присвоении
                # Остальные 77 полей с тестовыми данными
            ]
            row_data.extend([f"Данные{i}" for _ in range(len(self.HEADERS) - len(row_data))])
            ws.append(row_data)

        wb.save(file_path)
        self.stdout.write(self.style.SUCCESS(f"Файл создан: {file_path}"))
