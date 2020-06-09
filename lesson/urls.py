from django.urls import include, path

from lesson.views import *

urlpatterns = [
    path('', ListLessons.as_view()),
    path('generate/<int:pk>', GenerateLesson.as_view()),
    path('answer/<int:card_pk>/<int:is_correct>', AnswerCard.as_view()),
    path('bury/<int:card_pk>', BuryCard.as_view()),
    path('unbury/<int:card_pk>', UnburyCard.as_view())
]
