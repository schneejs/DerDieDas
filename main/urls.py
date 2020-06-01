from django.urls import include, path

from main.views import *

urlpatterns = [
    path('', ListLessons.as_view()),
    path('generate/<int:pk>/', GenerateLesson.as_view()),
]
