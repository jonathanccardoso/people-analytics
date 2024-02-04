from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from setup.utils import generate_months
from turnover.utils import generate_turnover, generate_series_turnover


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
        return Response({}, status=status.HTTP_200_OK)
