from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q

from setup.utils import generate_months
from turnover.models import Turnover
from turnover.utils import generate_turnover, generate_series_turnover, get_infos_by_company


class TurnoverInPeriod(APIView):
    def get(self, request, *args, **kwargs):
        init_date = request.query_params.get('init_date', None)
        end_date = request.query_params.get('end_date', None)

        if not init_date or not end_date:
            return Response({'error': 'Both init_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if init_date > end_date:
            return Response({'error': 'init_date cannot be greater than end_date.'}, status=status.HTTP_400_BAD_REQUEST)

        months = generate_months(init_date, end_date)
        turnover_results = generate_turnover(init_date, months)
            
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
                "series": generate_series_turnover(init_date, months, turnover_results)
            },
            "title": "Taxa de Turnover por Ano (%)",
            "grid": 6,
            "color": [
                "#D4DDE2",
                "#A3B6C2"
            ]
        }

        return Response(response_data, status=status.HTTP_200_OK)

class TurnoverInPeriodGraph(APIView):
    def get(self, request, *args, **kwargs):
        init_date = request.query_params.get('init_date', None)
        end_date = request.query_params.get('end_date', None)
        category = request.query_params.get('category', None)

        if not init_date or not end_date:
            return Response({'error': 'Both init_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if init_date > end_date:
            return Response({'error': 'init_date cannot be greater than end_date.'}, status=status.HTTP_400_BAD_REQUEST)

        employees = Turnover.objects.filter(
            Q(ds_category_1=category) | Q(ds_category_2=category) | Q(ds_category_3=category) | Q(ds_category_4=category) | Q(ds_category_5=category),
            fg_dismissal_on_month=1,
            dt_reference_month__range=[init_date, end_date]
        )

        companies_name, turnover_by_company = get_infos_by_company(init_date, end_date, employees)

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
                        "data": turnover_by_company,
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
