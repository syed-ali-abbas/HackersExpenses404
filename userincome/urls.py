from django.urls import path
from .views import add_income, Index, income_edit,income_delete, search_income, income_source_summary,income_stats_View
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('',Index,name='income'),
    path('add-income',add_income,name='add-income'),
    path('income_edit/<int:pk>',income_edit,name='income_edit'),
    path('income-delete/<int:pk>',income_delete,name='income-delete'),
    path('search_income',csrf_exempt(search_income),name='search_income'),
    path('income_source_summary',income_source_summary,name='income_source_summary'),
    path('income_stats_View',income_stats_View,name='income_stats_View')

]