from django.urls import include, path

from card.views import *

urlpatterns = [
    path('answer/<int:card_pk>/<int:is_correct>', AnswerCard.as_view()),
    path('bury/<int:card_pk>', BuryCard.as_view()),
    path('unbury/<int:card_pk>', UnburyCard.as_view())
]