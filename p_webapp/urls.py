from django.urls import path
from .views import add_expense#, Index


urlpatterns=[
    # path('',Index,name='index'),
    path('',add_expense,name='add-expense')
]