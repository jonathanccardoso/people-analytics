from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Headcount

from headcount.utils import generate_month_array, generate_series_array


class HeadcountInPeriod(APIView):
    def get(self, request, *args, **kwargs):
        init_date = request.query_params.get('init_date', None)
        end_date = request.query_params.get('end_date', None)

        if not init_date or not end_date:
            return Response({'error': 'Both init_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if init_date > end_date:
            return Response({'error': 'init_date cannot be greater than end_date.'}, status=status.HTTP_400_BAD_REQUEST)

        employees = Headcount.objects.filter(
            fg_status=1,
            dt_reference_month__range=[init_date, end_date]
        )
        months = generate_month_array(init_date, end_date)
        monthly_employee_count = [0] * len(months)
        for employee in employees:
            month = employee.dt_reference_month.month
            monthly_employee_count[month - 1] += 1

        response_data = {
            "xAxis": {
                "type": "category",
                "data": months
            },
            "yAxis": {
                "type": "value"
            },
            "series": {
                "type": "stacked_line",
                "series": generate_series_array(init_date, months, monthly_employee_count)
            },
            "title": "Headcount por Ano",
            "grid": 6,
            "color": [
                "#D4DDE2",
                "#A3B6C2"
            ]
        }

        return Response(response_data, status=status.HTTP_200_OK)
