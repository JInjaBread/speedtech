from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
import requests
import string
from django.utils import timezone
import random
from twilio.rest import Client
from .models import *
from .PhoneBackend import PhoneBackend
from django.shortcuts import get_object_or_404

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
    if request.user.is_authenticated:
        user = Costumer.objects.get(admin=request.user)
        cart = OrderItem.objects.filter(user_id=user.id)
        company = Company.objects.all()
        category = Category.objects.all()
        updated_product = Product.objects.all().order_by('-updated_at')[:10:1]
        new_product = Product.objects.all().order_by('-created_at')[:10:1]
        order_count = 0
        order_obj = []
        order = Order.objects.filter(user_id=user.id)
        for order in order:
            order = Order.objects.get(id=order.id)
            if order.ref_code != None:
                order_count = order_count + 1
                order_obj.append(order)
            else:
                pass
        context = {
            "company":company,
            "category":category,
            "updated_product":updated_product,
            "new_product":new_product,
            "cart":cart,
            "order_count":order_count
        }
    else:
        company = Company.objects.all()
        category = Category.objects.all()
        updated_product = Product.objects.all().order_by('-updated_at')[:10:1]
        new_product = Product.objects.all().order_by('-created_at')[:10:1]
        context = {
            "company":company,
            "category":category,
            "updated_product":updated_product,
            "new_product":new_product,
        }
    return render(request, 'landing.html', context)

def loginpage(request):

    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = PhoneBackend.authenticate(request, username = request.POST.get('username'), password = request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                #return redirect('')
                pass
            elif user_type == '2':
                # return HttpResponse("Staff Login")
                #return redirect('staff_home')
                pass
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')

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
    return render(request, 'signup.html')

def verify_otp(request):
    if request.method == 'POST':
        temp_otp = request.POST.get('otp_v')
        otp = request.session['otp']
        print(temp_otp)
        print(otp)
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
                return redirect('login')
            except Exception as e:
                print(e)
                return redirect('login')
        else:
            print('False')
            return redirect('verify_otp')
    return render(request, 'verify_otp.html')

def motorcycle(request):
    if request.user.is_authenticated:
        user = Costumer.objects.get(admin=request.user)
        cart = OrderItem.objects.filter(user_id=user.id)
        motorcycle = Motorcycle.objects.all()
        category = Category.objects.all()
        order_count = 0
        order_obj = []
        order = Order.objects.filter(user_id=user.id)
        for order in order:
            order = Order.objects.get(id=order.id)
            if order.ref_code != None:
                order_count = order_count + 1
                order_obj.append(order)
            else:
                pass
        context = {
        "category": category,
        "motorcycle": motorcycle,
        "cart":cart,
        "order_count":order_count
        }
    else:
        motorcycle = Motorcycle.objects.all()
        category = Category.objects.all()
        context = {
        "category": category,
        "motorcycle": motorcycle,
        }
    return render(request, 'motorcycle.html', context)

def motorcycle_company(request, company_id):
    if request.user.is_authenticated:
        user = Costumer.objects.get(admin=request.user)
        cart = OrderItem.objects.filter(user_id=user.id)
        category = Category.objects.all()
        company = Company.objects.get(id=company_id)
        motorcycle = Motorcycle.objects.filter(company=company.id)
        order_count = 0
        order_obj = []
        order = Order.objects.filter(user_id=user.id)
        for order in order:
            order = Order.objects.get(id=order.id)
            if order.ref_code != None:
                order_count = order_count + 1
                order_obj.append(order)
            else:
                pass
        context = {
        "motorcycle": motorcycle,
        "company": company,
        "category": category,
        "cart":cart,
        "order_count":order_count
        }
    else:
        category = Category.objects.all()
        company = Company.objects.get(id=company_id)
        motorcycle = Motorcycle.objects.filter(company=company.id)
        order_count = 0
        order_obj = []
        order = Order.objects.filter(user_id=user.id)
        for order in order:
            order = Order.objects.get(id=order.id)
            if order.ref_code != None:
                order_count = order_count + 1
                order_obj.append(order)
            else:
                pass
        context = {
        "motorcycle": motorcycle,
        "company": company,
        "category": category,
        "order_count": order_count
        }
    return render(request, 'motorcycle.html', context)

def product(request):
    if request.user.is_authenticated:
        user = Costumer.objects.get(admin=request.user)
        cart = OrderItem.objects.filter(user_id=user.id)
        category = Category.objects.all()
        product = Product.objects.all()
        order_count = 0
        order_obj = []
        order = Order.objects.filter(user_id=user.id)
        for order in order:
            order = Order.objects.get(id=order.id)
            if order.ref_code != None:
                order_count = order_count + 1
                order_obj.append(order)
            else:
                pass
        context = {
        "category": category,
        "product": product,
        "cart": cart,
        "order_count":order_count
        }
    else:
        category = Category.objects.all()
        product = Product.objects.all()
        context = {
        "category": category,
        "product": product,
        }

    return render(request, 'product.html', context)

def product_category(request, category_id):
    category = Category.objects.all()
    category_temp = category.get(id=category_id)
    product = Product.objects.filter(category=category_temp.id)
    context = {
    "category": category,
    "product": product,
    }
    return render(request, 'product.html', context)

def cart(request):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    category = Category.objects.all()
    total = 0
    order_count = 0
    order_obj = []
    order = Order.objects.filter(user_id=user.id)
    for order in order:
        order = Order.objects.get(id=order.id)
        if order.ref_code != None:
            order_count = order_count + 1
            order_obj.append(order)
        else:
            pass
    if cart.count() == '0':
        context = {
            "cart":cart,
            "total":total,
            "category":category,
            "order_count":order_count
        }
    else:
        for item in cart:
            price = cart.get(item_id=item.item.id)
            price_2 = price.get_total_item_price()
            total = total + price_2

        context = {
            "cart":cart,
            "total":total,
            "category":category,
            "order_count":order_count
        }

    return render(request, 'cart.html', context)

def update_cart(request, item_id):
    if request.method == 'POST':
        user = Costumer.objects.get(admin=request.user)
        cart = OrderItem.objects.filter(user_id=user.id)
        cart_to_update = cart.get(id=item_id)
        quantity = request.POST.get('quantity')
        if quantity != '0':
            try:
                cart_to_update.quantity = quantity
                cart_to_update.save()
                return redirect(request.META['HTTP_REFERER'])
            except:
                print('error')
                return redirect(request.META['HTTP_REFERER'])
        else:
            try:
                cart_to_update.quantity = 1
                cart_to_update.save()
                return redirect(request.META['HTTP_REFERER'])
            except:
                print('error')
                return redirect(request.META['HTTP_REFERER'])


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = Costumer.objects.get(admin=request.user)
    order_item, created = OrderItem.objects.get_or_create(
        item=product,
        user=user,
        ordered=False
    )
    order_qs = OrderItem.objects.filter(user=user.id, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.item.id == product.id:
            messages.info(request, "This item is on your cart allready.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            print('This')
            messages.info(request, "This item was added to your cart.")
            return redirect(request.META['HTTP_REFERER'])

    else:
        cart = OrderItem(
            item=product,
            user=user,
            ordered=False
        )
        cart.save()
        messages.info(request, "This item was added to your cart.")
        return redirect(request.META['HTTP_REFERER'])

def remove_from_cart(request, item_id):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    cart_to_delete = cart.get(id=item_id)
    try:
        cart_to_delete.delete()
        messages.info(request, "Item was deleted to cart!.")
        return redirect(request.META['HTTP_REFERER'])
    except:
        cart_to_delete.delete()
        messages.info(request, "Error!.")
        return redirect(request.META['HTTP_REFERER'])

def make_order(request):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    ref_code = create_ref_code()
    list = ""
    total = 0
    for item in cart:
        price = cart.get(item_id=item.item.id)
        price_2 = price.get_total_item_price()
        total = total + price_2
    try:
        order = Order(user=user, ref_code=ref_code, total=total)
        for item in cart:
            print(item.id)
            list = list + ", " +str(item)
            product = Product.objects.get(id=item.item.id)
            product.stock = product.stock - item.quantity
            product.save()
        list = list[1:]
        order.items = list
        order.save()
        messages.info(request, "ORDER IS SET!!.")
        return redirect(request.META['HTTP_REFERER'])
    except Exception as e:
        print(e)
        messages.info(request, "Error!!.")
        return redirect(request.META['HTTP_REFERER'])

def order(request):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    category = Category.objects.all()
    order_count = 0
    order_obj = []
    order = Order.objects.filter(user_id=user.id)
    for order in order:
        print(order.items)
        order = Order.objects.get(id=order.id)
        if order.ref_code != None:
            order_count = order_count + 1
            order_obj.append(order)
        else:
            pass
    context = {
        "user":user,
        "cart":cart,
        "category":category,
        "order_obj":order_obj,
        "order_count": order_count,

    }
    return render(request, 'order.html', context)
