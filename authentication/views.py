from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.urls import reverse
import threading


class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)




class RegisterationView(View):
    def get(self, request):
        return render(request,'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print(username,email,password)
        context = {
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'Password Length should be greater than 6 characters')
                    return render(request,'authentication/register.html',context)
                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                messages.success(request,'Account Created Successfully')
                return redirect('login-view')
        return render(request,'authentication/register.html')


class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username,password=password)
            if user:
                # if auth.is_active():
                auth.login(request,user)
                messages.success(request,"Success")
                return redirect('expenses')

                
                # messages.error(request,"Error not active user found")
                # return render(request,'authentication/login.html')

            messages.error(request,"Invalid Credentials")
            return render(request,'authentication/login.html')

        messages.error(request,"Please Fill all fields")
        return render(request,'authentication/login.html')
        

class SignOut(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request,"Loged Out Successfully")
        return redirect('login-view')



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
        

        return JsonResponse({'Success': True},status=200)





class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')

    def post(self,request):
        email = request.POST['email']
        context={
            'values':request.POST
        }
        if not validate_email(email):
            messages.error(request,'Please enter a valid Email')
            return render(request,'authentication/reset-password.html',context)

        current_site = get_current_site(request)
        user=User.objects.filter(email=email)
        if user.exists():
            email_content = {
                    'user': user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token': PasswordResetTokenGenerator().make_token(user[0]),
                }

            link = reverse('set-new-password', kwargs={
                               'uidb64': email_content['uid'], 'token': email_content['token']})

            email_subject = 'Passworf Reset Instructions'

            reset_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                    email_subject,
                    'Hi  there, Please the link below to reset your password \n'+reset_url,
                    'noreply@semycolon.com',
                    [email],
                )
            EmailThread(email).start()
            
            messages.success(request,'You will recieve a Reset Password Link If you are Registered')


            return render(request,'authentication/reset-password.html',context)


class CompletePasswordReset(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        return render(request,'authentication/set-new-password.html',context)


    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['password']
        confirmpassword=request.POST['password2']
        if password!=confirmpassword:
            messages.error(request,'Passwords not matching')
            return render(request,'authentication/set-new-password.html',context)
        if len(password)<6:
            messages.error(request,'Password Too Short')
            return render(request,'authentication/set-new-password.html',context)

        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Changed Sucessfully')
            return redirect('login-view')
        except Exception as identifier:
            messages.info(request,"Ooop's Something went wrong")
            return render(request,'authentication/set-new-password.html',context)

        
        # return render(request,'authentication/set-new-password.html',context)


        
        
            



        