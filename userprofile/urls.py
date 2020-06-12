from django.urls import include, re_path

from userprofile.views import *

urlpatterns = [
    re_path(r'^(?P<username>\w*)$', Profile.as_view())
]
