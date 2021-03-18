from django.urls import path
from .views import RegisterationView

urlpatterns=[
    path('register',RegisterationView.as_view(),name='register')
]