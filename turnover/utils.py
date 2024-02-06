from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from headcount.utils import get_first_and_last_day
from turnover.models import Turnover


def generate_turnover(init_date, months):
    turnover_results = []

    for index, _ in enumerate(months):
        if index != 0:
            current_date = datetime.strptime(init_date, '%Y-%m-%d')
            next_month_date = current_date + relativedelta(months=1)
            init_date = next_month_date.strftime('%Y-%m-%d')

        month_start_date, month_end_date = get_first_and_last_day(init_date)

        employees_dismissal_length = Turnover.objects.filter(
            fg_dismissal_on_month=1,
            dt_reference_month__range=[month_start_date, month_end_date]
        ).count()

        employees_active_length = Turnover.objects.filter(
            fg_status=1,
            dt_reference_month__range=[month_start_date, month_end_date]
        ).count()

        # avoid division by zero
        turnover_result = employees_dismissal_length / (employees_active_length or 1)
        turnover_result = round(turnover_result, 2)

        turnover_results.append(turnover_result)
    
    return turnover_results

def generate_series_turnover(init_date, months, turnover_results):
    current_year = datetime.strptime(init_date, '%Y-%m-%d').year
    turnover_in_year = [
        turnover_results[i:i + 12] for i in range(0, len(turnover_results), 12)
    ]
    series = []

    for month in months:
        if month == "Jan":
            year = current_year + 1 if len(series) else current_year

            current_data = turnover_in_year[len(series) - 1]

            series.append({
                "name": year,
                "type": "line",
                "data": current_data
            })

    return series

def get_infos_by_company(init_date, end_date, category, employees):
    companies_name = list(employees.values_list('ds_category_1', flat=True).distinct())

    company_counts = {}
    for company_name in companies_name:
        employees_dismissal_length = Turnover.objects.filter(
            Q(ds_category_1=category) | Q(ds_category_2=category) | Q(ds_category_3=category) | Q(ds_category_4=category) | Q(ds_category_5=category),
            ds_category_1=company_name,
            fg_dismissal_on_month=1,
            dt_reference_month__range=[init_date, end_date]
        ).count()

        employees_active_length = Turnover.objects.filter(
            Q(ds_category_1=category) | Q(ds_category_2=category) | Q(ds_category_3=category) | Q(ds_category_4=category) | Q(ds_category_5=category),
            ds_category_1=company_name,
            fg_status=1,
            dt_reference_month__range=[init_date, end_date]
        ).count()

        # avoid division by zero
        turnover_result = employees_dismissal_length / (employees_active_length or 1)
        turnover_result = round(turnover_result, 2)

        company_counts[company_name] = turnover_result

    turnover_by_company = [count for _, count in company_counts.items()]

    return companies_name, turnover_by_company