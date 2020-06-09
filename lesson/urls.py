from django.urls import include, path

from lesson.views import *

urlpatterns = [
    path('', ListLessons.as_view()),
    path('generate/<int:pk>', GenerateLesson.as_view())
]
