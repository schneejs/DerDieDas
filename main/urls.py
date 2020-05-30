from django.urls import path, include

from main.views import *

urlpatterns = [
    path('', ListLessons.as_view()),
    path('<int:pk>/', GenerateLesson.as_view()),
]
