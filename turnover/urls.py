from django.urls import path
from .views import TurnoverInPeriod, TurnoverInPeriodGraph

urlpatterns = [
    path('line_chart/', TurnoverInPeriod.as_view(), name='TurnoverInPeriod-line-chart'),
    path('category_charts/', TurnoverInPeriodGraph.as_view(), name='TurnoverInPeriod-graph-chart'),
]
