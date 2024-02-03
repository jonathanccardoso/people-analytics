from django.urls import path
from .views import HeadcountInPeriod

urlpatterns = [
    path('line_chart/', HeadcountInPeriod.as_view(), name='HeadcountInPeriod-line-chart'),
]
