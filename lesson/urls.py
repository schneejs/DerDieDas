from django.urls import include, path

from lesson.views import *

urlpatterns = [
    path('list', ListLessons.as_view()),
    path('generate/<int:pk>', GenerateLesson.as_view()),
    path('create', CreateLesson.as_view()),
    path('delete/<int:pk>', DeleteLesson.as_view()),
    path('update/<int:pk>', UpdateLesson.as_view())
]
