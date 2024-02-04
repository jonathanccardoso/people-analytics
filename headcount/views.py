from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q

from setup.utils import generate_months
from headcount.utils import generate_series, get_first_and_last_day, get_infos_from_company
from .models import Headcount


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
        months = generate_months(init_date, end_date)
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
                "series": generate_series(init_date, months, monthly_employee_count)
            },
            "title": "Headcount por Ano",
            "grid": 6,
            "color": [
                "#D4DDE2",
                "#A3B6C2"
            ]
        }

        return Response(response_data, status=status.HTTP_200_OK)

class HeadcountInLastPeriod(APIView):
    def get(self, request, *args, **kwargs):
        init_date = request.query_params.get('init_date', None)
        end_date = request.query_params.get('end_date', None)
        category = request.query_params.get('category', None)

        if not init_date or not end_date or not category:
            return Response({'error': 'Both init_date, end_date and category are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if init_date > end_date:
            return Response({'error': 'init_date cannot be greater than end_date.'}, status=status.HTTP_400_BAD_REQUEST)

        first_day_of_month, last_day_of_month = get_first_and_last_day(end_date)

        employees = Headcount.objects.filter(
            Q(ds_category_1=category) | Q(ds_category_2=category) | Q(ds_category_3=category) | Q(ds_category_4=category) | Q(ds_category_5=category),
            fg_status=1,
            dt_reference_month__range=[first_day_of_month, last_day_of_month],
        )
        companies_name, employee_counts_by_company = get_infos_from_company(employees)

        response_data = {
            "xAxis": {
                "type": "value",
                "show": True,
                "max": {}
            },
            "yAxis": {
                "type": "category",
                "data": companies_name
            },
            "series": {
                "type": "horizontal_stacked",
                "series": [
                    {
                        "name": "Colaboradores",
                        "data": employee_counts_by_company,
                        "type": "bar"
                    }
                ]
            },
            "title": "Empresa",
            "grid": 6,
            "color": [
                "#2896DC"
            ],
            "is%": False
        }

        return Response(response_data, status=status.HTTP_200_OK)

