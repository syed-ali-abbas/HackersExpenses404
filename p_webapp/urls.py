from django.urls import path
from .views import add_expense, Index, expense_edit,expense_delete


urlpatterns=[
    path('',Index,name='expenses'),
    path('add-expenses',add_expense,name='add-expense'),
    path('expense_edit/<int:pk>',expense_edit,name='expense_edit'),
    path('expense-delete/<int:pk>',expense_delete,name='expense-delete')
]