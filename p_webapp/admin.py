from django.contrib import admin
from .models import Category, Expense
# Register your models here.



class ExpenseAdmin(admin.ModelAdmin):
    list_display=('amount','descripption','owner','category','date',)
    search_fields=('amount','descripption','category','date',)
    list_per_page=5








admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Category)