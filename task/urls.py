from django.urls import path
from .views import loginapi,signupapi,logoutapi,taskapi,expiredapi

urlpatterns = [
    path('',loginapi.as_view()),
    path('signup/',signupapi.as_view()),
    path('logout/',logoutapi.as_view()),
    path('task/',taskapi.as_view()),
    path('expired/',expiredapi.as_view())
]