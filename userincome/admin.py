from django.contrib import admin
from .models import UserIncome,Source
# Register your models here.

class UserIncomeAdmin(admin.ModelAdmin):
    list_display=('amount','source','descripption','owner','date')
    search_fields=('amount','source','descripption','date')



admin.site.register(UserIncome,UserIncomeAdmin)
admin.site.register(Source)
