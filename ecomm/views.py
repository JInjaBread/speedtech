from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
import requests
import string
import random
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from .models import *
from .PhoneBackend import PhoneBackend
from django.shortcuts import get_object_or_404
from . import CostumerViews
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# Create your views here.
def send_otp(phone, otp):
    client = Client(settings.ACCOUNT_SID, settings.ACCOUNT_SECURITY_API_KEY)
    message = client.messages.create(
                              messaging_service_sid='MGfff7d060816fff6943af74d9cd59fc3b',
                              body='Your otp is ' + str(otp),
                              to=phone
                          )
    print(message.sid)

def home(request):
    user = request.user
    print(user)

    return render(request, 'landing.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = PhoneBackend.authenticate(request, username = request.POST.get('username'), password = request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('costumer_home')
            else:
                messages.error(request, "Invalid Credentials!")
                return redirect('home')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        otp_req = random.randint(1111, 9999)
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['phone'] = request.POST.get('username')
        request.session['address'] = request.POST.get('address')
        request.session['password'] = request.POST.get('password')
        request.session['otp'] = otp_req
        send_otp(request.session['phone'], otp_req)
        return redirect('verify_otp')

def verify_otp(request):
    phone = request.session['phone']
    context = {
    "phone":phone
    }
    otp = request.session['otp']
    print(otp)
    if request.method == 'POST':
        temp_otp = request.POST.get('otp_v')
        otp = request.session['otp']
        if temp_otp == str(otp):
            first_name = request.session['first_name']
            last_name = request.session['last_name']
            phone = request.session['phone']
            address = request.session['address']
            password = request.session['password']
            try:
                user = CustomUser.objects.create_user(username=phone, password=password, first_name=first_name, last_name=last_name, user_type=3)
                user.costumer.address = address
                user.save()
                print('save')
                return redirect('home')
            except Exception as e:
                print(e)
                return redirect('home')
        else:
            print('False')
            return redirect('verify_otp')
    return render(request, 'verify_otp.html', context)

@csrf_exempt
def check_phone_exist(request):
    phone = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=phone).exists()
    if user_obj:
        return JsonResponse({'response':'error', 'message':'True'})
    else:
        return JsonResponse({'response':'error', 'message':'False'})
