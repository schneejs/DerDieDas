from django.urls import path, include

from userprofile.views import *

urlpatterns = [
    path('<str:username>/', ProfileByUsername.as_view())
]