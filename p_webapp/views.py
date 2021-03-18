from django.shortcuts import render

# Create your views here.
# def Index(request):
#     return render(request, 'base.html')


def add_expense(request):
    return render(request, 'expense/index.html')