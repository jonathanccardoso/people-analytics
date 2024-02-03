from datetime import datetime, timedelta


def generate_month_array(init_date, end_date):
    init_date_obj = datetime.strptime(init_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    current_month = init_date_obj.replace(day=1)
    months = []

    while current_month <= end_date_obj:
        months.append(current_month.strftime('%b')) # name month
        current_month = (current_month + timedelta(days=32)).replace(day=1)
    
    return months

def generate_series_array(init_date, months, monthly_employee_count):
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
