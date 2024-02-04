from datetime import datetime, timedelta

def generate_months(init_date, end_date):
    init_date_obj = datetime.strptime(init_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    current_month = init_date_obj.replace(day=1)
    months = []

    while current_month <= end_date_obj:
        months.append(current_month.strftime('%b')) # name month
        current_month = (current_month + timedelta(days=32)).replace(day=1)
    
    return months
