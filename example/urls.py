from django.urls import path
from example.views import *


urlpatterns = [
    path('search/<str:word>', FindExamples.as_view()),
    path('<int:pk>', ExampleView.as_view())
]