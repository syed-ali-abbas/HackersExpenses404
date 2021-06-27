from django.urls import path
from .views import add_expense, Index, expense_edit,expense_delete, search_expenses, expense_category_summary,stats_View, export_CSV,export_EXCEL
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('',Index,name='expenses'),
    path('add-expenses',add_expense,name='add-expense'),
    path('expense_edit/<int:pk>',expense_edit,name='expense_edit'),
    path('expense-delete/<int:pk>',expense_delete,name='expense-delete'),
    path('search-expenses',csrf_exempt(search_expenses),name='search-expenses'),
    path('expense_category_summary',expense_category_summary,name='expense_category_summary'),
    path('stats',stats_View,name='stats'),
    path('export-csv',export_CSV,name='export-csv'),
    path('export-excel',export_EXCEL,name='export-excel')

]