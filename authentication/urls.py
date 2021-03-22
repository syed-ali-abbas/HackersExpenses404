from django.urls import path
from .views import RegisterationView, userNameValidationView, EmailValidationView, LoginView,SignOut
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('register',RegisterationView.as_view(),name='register'),
    path('validate-username', csrf_exempt(userNameValidationView.as_view()),name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name='validate-email'),
    path('login-view', LoginView.as_view(),name='login-view'),
    path('SignOut', SignOut.as_view(),name='SignOut')
]