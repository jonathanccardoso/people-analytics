from datetime import datetime
import calendar


def generate_series(init_date, months, monthly_employee_count):
    current_year = datetime.strptime(init_date, '%Y-%m-%d').year
    employee_in_year = [
        monthly_employee_count[i:i + 12] for i in range(0, len(monthly_employee_count), 12)
    ]
    series = []

    for month in months:
        if month == "Jan":
            year = current_year + 1 if len(series) else current_year

            current_data = employee_in_year[len(series)]

            series.append({
                "name": year,
                "type": "line",
                "data": current_data
            })

    return series

def get_first_and_last_day(date_str):
    input_date = datetime.strptime(date_str, '%Y-%m-%d')

    first_day_of_month = input_date.replace(day=1)

    _, last_day_of_month = calendar.monthrange(first_day_of_month.year, first_day_of_month.month)
    last_day_of_month = first_day_of_month.replace(day=last_day_of_month)

    formatted_first_day = first_day_of_month.strftime('%Y-%m-%d')
    formatted_last_day = last_day_of_month.strftime('%Y-%m-%d')

    return formatted_first_day, formatted_last_day

def get_infos_from_company(employees):
    companies_name = list(employees.values_list('ds_category_1', flat=True).distinct())

    company_counts = {}
    for employee in employees:
        company_name = employee.ds_category_1
        company_counts[company_name] = company_counts.get(company_name, 0) + 1

    employee_counts_by_company = [count for _, count in company_counts.items()]

    return companies_name, employee_counts_by_company