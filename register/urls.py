from django.urls import path, re_path

from register.views import *

urlpatterns = [
    path('languages', Languages.as_view()),
    path('', SignUp.as_view())
]
