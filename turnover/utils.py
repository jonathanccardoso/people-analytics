from datetime import datetime
from dateutil.relativedelta import relativedelta

from headcount.utils import get_first_and_last_day
from turnover.models import Turnover


def generate_series(init_date, months, monthly_employee_count):
    current_year = datetime.strptime(init_date, '%Y-%m-%d').year
    employee_in_year = [
        monthly_employee_count[i:i + 12] for i in range(0, len(monthly_employee_count), 12)
    ]
    series = []
    current_data = []

    for month in months:
        if month == "Jan":
            current_data = []
            year = current_year + 1 if len(series) else current_year

            series.append({
                "name": year,
                "type": "line",
                "data": current_data
            })

            current_data.append(employee_in_year[len(series) - 1])

    return series

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
    current_data = []

    for month in months:
        if month == "Jan":
            current_data = []
            year = current_year + 1 if len(series) else current_year

            series.append({
                "name": year,
                "type": "line",
                "data": current_data
            })

            current_data.append(turnover_in_year[len(series) - 1])

    return series