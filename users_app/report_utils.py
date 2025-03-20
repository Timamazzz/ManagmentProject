from datetime import date
from django.db.models import Q


def get_volunteers_for_report(queryset, start_date: date, end_date: date):
    """
    Фильтрует переданный QuerySet добровольцев, работающих в заданном периоде.

    :param queryset: QuerySet добровольцев.
    :param start_date: Дата начала периода.
    :param end_date: Дата конца периода.
    :return: QuerySet отфильтрованных добровольцев.
    """
    if not start_date or not end_date:
        raise ValueError("Необходимо указать start_date и end_date.")

    queryset = queryset.exclude(dismissal_date__isnull=False, dismissal_date__lte=start_date)
    queryset = queryset.filter(enrollment_date__lte=end_date)
    queryset = queryset.exclude(remarks__date__range=(start_date, end_date))

    return queryset


def get_worked_days(volunteer, start_date: date, end_date: date) -> int:
    """
    Вычисляет количество отработанных дней добровольца в заданном периоде.

    :param volunteer: Объект добровольца (из модели).
    :param start_date: Дата начала периода.
    :param end_date: Дата конца периода.
    :return: Количество отработанных дней.
    """
    if not start_date or not end_date:
        raise ValueError("Необходимо указать start_date и end_date.")

    active_start = max(start_date, volunteer.enrollment_date)
    active_end = min(end_date, volunteer.dismissal_date) if volunteer.dismissal_date else end_date

    return (active_end - active_start).days + 1 if active_start <= active_end else 0
