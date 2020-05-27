from django.urls import path
from example.views import *


urlpatterns = [
    path('<str:word>/', FindExamples.as_view())
]