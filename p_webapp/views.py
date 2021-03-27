from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
# Create your views here.
@login_required(login_url='/authentication/login-view')
def Index(request):
    categories= Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    context={
        'expenses':expenses
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

