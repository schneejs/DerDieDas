from django.urls import path
from battery.views import *


urlpatterns = [
    path('', BatteryView.as_view())
]