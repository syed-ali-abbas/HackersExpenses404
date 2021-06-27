from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userprefences.models import UserPreference
import csv
import datetime
import xlwt
# Create your views here.



def search_expenses(request):
    if request.method=='POST':
        search_str=json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str,owner=request.user)|Expense.objects.filter(date__istartswith=search_str,owner=request.user)|Expense.objects.filter(descripption__icontains=search_str,owner=request.user)|Expense.objects.filter(category__istartswith=search_str,owner=request.user)
        data = expenses.values()

        return JsonResponse(list(data),safe=False)





@login_required(login_url='/authentication/login-view')
def Index(request):
    categories= Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context={
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'expense/index.html',context)


@login_required(login_url='/authentication/login-view')
def add_expense(request):
    categories= Category.objects.all()
    context = {
        'categories':categories,
        'values':request.POST
    }
    if request.method == 'GET':
        return render(request, 'expense/add_expense.html',context)
    

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']
        if not amount:
            messages.error(request,'Field Amount is Empty. Please try again')
            return render(request, 'expense/add_expense.html',context)
    

        if not description:
            messages.error(request,'Description Amount is Empty. Please try again')
            return render(request, 'expense/add_expense.html',context)

        Expense.objects.create(owner=request.user,amount=amount,date=date,category=category,descripption=description)
        messages.success(request,'Expense saved successfully')

        return redirect('expenses')


def expense_edit(request,pk):
    categories= Category.objects.all()
    expense = Expense.objects.get(pk=pk)
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories
    }
    if request.method=='GET':
        
        return render(request, 'expense/edit-expense.html',context)

    if request.method=='POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']
        if not amount:
            messages.error(request,'Field Amount is Empty. Please try again')
            return render(request, 'expense/edit-expense.html',context)
    

        if not description:
            messages.error(request,'Description Amount is Empty. Please try again')
            return render(request, 'expense/edit-expense.html',context)

        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.descripption=description
        expense.save()
        messages.success(request,'Expense Updated successfully')
        return redirect('expenses')


def expense_delete(request,pk):
    expense=Expense.objects.get(pk=pk)
    expense.delete()
    messages.success(request,'Expense Removed Successfully')
    return redirect('expenses')




def expense_category_summary(request):
    finalrep = {}
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user)
    # print('expense_category_summary',six_months_ago)

    def get_category(expenses):
        return expenses.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)








def stats_View(request):
    return render(request, 'expense/stats.html')





def export_CSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.today())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses=Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.descripption,expense.category,expense.date])

    return response



def export_EXCEL(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.today())+'.xls'
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet=workbook.add_sheet('Expenses')
    row_num = 0
    fontstyle=xlwt.XFStyle()
    fontstyle.font.bold=True
    column=['Amount','Description','Category','Date']

    for col_num in range(len(column)):
        worksheet.write(row_num,col_num, column[col_num],fontstyle)

    fontstyle=xlwt.XFStyle()
    rows=Expense.objects.filter(owner=request.user).values_list('amount','descripption','category','date')
    for row in rows:
        row_num+=1 
        for col_num in range(len(row)):
            worksheet.write(row_num,col_num,str(row[col_num]),fontstyle)

    workbook.save(response)


    return response


