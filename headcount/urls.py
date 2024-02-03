from django.urls import path
from .views import HeadcountInPeriod, HeadcountInLastPeriod

urlpatterns = [
    path('line_chart/', HeadcountInPeriod.as_view(), name='HeadcountInPeriod-line-chart'),
    path('category_charts/', HeadcountInLastPeriod.as_view(), name='HeadcountInPeriod-graph-chart'),
]
