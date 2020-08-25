from django.urls import include, path, re_path

from userprofile.views import *

urlpatterns = [
    re_path(r'^(?P<username>\w*)$', Profile.as_view()),
    path('password/change', ChangePassword.as_view())
]
