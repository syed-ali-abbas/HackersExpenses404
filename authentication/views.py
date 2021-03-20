from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages






class RegisterationView(View):
    def get(self, request):
        return render(request,'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # GET user data
        #Validate
        # Create User Account
        # messages.success(request,'Success Whats Up')
        # messages.warning(request,'Success Whats Up war')
        # messages.info(request,'Success Whats Up info')
        # messages.error(request,'Success Whats Up error')
        return render(request,'authentication/register.html')



class userNameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Matching username exixts. Please try again with unique one'}, status=409)
        return JsonResponse({'username_valid':True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})