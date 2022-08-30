import json
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.contrib import messages
from twilio.rest import Client
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from decimal import *

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)

def send_notification(phone, ref_code):
    client = Client(settings.ACCOUNT_SID, settings.ACCOUNT_SECURITY_API_KEY)
    message = client.messages.create(
                              messaging_service_sid='MGfff7d060816fff6943af74d9cd59fc3b',
                              body='Your order with reference code ' + str(ref_code) + ' is ready for pickup',
                              to=phone
                          )
    print(message.sid)

def staff_home(request):
    order = Order.objects.all()
    order_obj = []
    for order in order:
        print(order.ref_code)
        if order.ref_code != None:
            order_obj.append(order)
    order_que = len(order_obj)
    company = Company.objects.all()
    motorcycle = Motorcycle.objects.all()
    products = Product.objects.all()
    context = {
        "order_que": order_que,
        "company": company,
        "motorcycle": motorcycle,
        "products": products
    }
    return render(request, 'staff/staff_home.html', context)

def costumer(request):
    costumer = Costumer.objects.all()
    context = {
        "costumer": costumer,
    }
    return render(request, 'staff/costumer.html', context)

def company(request):
    company = Company.objects.all()
    context = {
        "company": company,
    }
    return render(request, 'staff/company.html', context)

def add_company(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('company')
    else:
        name = request.POST.get('name')

        image_file = request.FILES['file']
    try:
        company = Company(name=name, image = image_file)
        company.save()
        messages.success(request, "Company Save Sucessfully")
        return redirect('company')
    except:
        messages.error(request, "Company Save Unsucessfull")
        return redirect('company')

def edit_company(request, company_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('company')
    else:
        company = Company.objects.get(id=company_id)
        name = request.POST.get('name')
        image_file = None
        if len(request.FILES) != 0:
            image_file = request.FILES['file']
        else:
            image_file = None

        if image_file == None:
            try:
                company.name = name
                company.save()
                messages.success(request, "Saved Succesfully")
                return redirect('company')
            except:
                messages.error(request, "Error on Submit")
                return redirect('company')
        else:
            try:
                company.name = name
                company.image = image_file
                company.save()
                messages.success(request, "Saved Succesfully")
                return redirect('company')
            except:
                messages.error(request, "Error on Submit")
                return redirect('company')

def motorcycle(request):
    company = Company.objects.all()
    motorcycle = Motorcycle.objects.all()
    context = {
        "motorcycle": motorcycle,
        "company": company
    }
    return render(request, 'staff/motorcycle.html', context)

def add_motorcycle(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('company')
    else:
        name = request.POST.get('name')
        company = request.POST.get('company')
        print(company)
        image_file = request.FILES['file']
        anatomy_image = request.FILES['anatomy']
        company_obj = Company.objects.get(id=company)

    try:
        motorcycle = Motorcycle(name=name, company = company_obj ,image = image_file, anatomy_image=anatomy_image)
        motorcycle.save()
        messages.success(request, "Motorcycle Save Sucessfully")
        return redirect('motorcycle')
    except:
        messages.error(request, "Motorcycle Save Unsucessfull")
        return redirect('motorcycle')



def products(request):
    motorcycle = Motorcycle.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "motorcycle": motorcycle
    }
    return render(request, 'staff/products.html', context)

def save_products(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('company')
    else:
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        motorcycle = request.POST.get('motorcycle')
        category = request.POST.get('category')
        image_file = request.FILES['file']

        motorcycle_obj = Motorcycle.objects.get(id=motorcycle)
        category_obj = Category.objects.get(id=category)

        try:
            product = Product(name=name, price=price, stock=stock,motorcycle=motorcycle_obj, category=category_obj, image = image_file )
            product.save()
            messages.success(request, "Product Save Sucessfully")
            return redirect('products')
        except Exception as e:
            print(e)
            messages.success(request, "Error Saving Products")
            return redirect('products')

def edit_product(request, product_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('motorcycle')
    else:
        product = Product.objects.get(id=product_id)
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        mt = request.POST.get('motorcycle')
        ct = request.POST.get('category')
        motorcycle = Motorcycle.objects.get(id=mt)
        category = Category.objects.get(id=ct)
        image_file = None
        if len(request.FILES) != 0:
            image_file = request.FILES['file']
        else:
            image_file = None

        if image_file == None:
            try:
                product.name = name
                product.price = price
                product.stock = stock
                product.motorcycle = motorcycle
                product.category = category
                product.save()
                messages.success(request, "Saved Succesfully")
                return redirect('products')
            except Exception as e:
                print(e)
                messages.error(request, "Error on Submit")
                return redirect('products')
        else:
            try:
                product.name = name
                product.price = price
                product.stock = stock
                product.motorcycle = motorcycle
                product.category = category
                Product.image = image_file
                product.save()
                messages.success(request, "Saved Succesfully")
                return redirect('products')
            except Exception as e:
                print(e)
                messages.error(request, "Error on Submit")
                return redirect('products')

def orders(request):
    order = Order.objects.all()
    context = {
        "order": order
    }
    return render(request, 'staff/order.html', context)

@csrf_exempt
def get_orders(request):
    order = Order.objects.all()
    data = []
    for order in order:
        t = str(order.total)
        total = Decimal(t)
        print(total)
        data_small = {"id": order.id, "ref_code": order.ref_code, "status": order.status, "total": total, "items": order.items, "first_name": order.user.admin.first_name, "last_name": order.user.admin.last_name}
        data.append(data_small)

    return JsonResponse(json.dumps(data, cls=DecimalEncoder), content_type="application/json", safe=False)

@csrf_exempt
def get_orders_data(request):
    id = request.POST.get('id')
    print(id)
    order = Order.objects.get(id=id)
    data = {"id": order.id, "ref_code": order.ref_code, "status": order.status, "total": order.total, "items": order.items, "first_name": order.user.admin.first_name, "last_name": order.user.admin.last_name}

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

@csrf_exempt
def set_ready(request):
    order_id = request.POST.get('id')
    print(order_id)
    order = Order.objects.get(id = order_id)

    try:
        order.status = "Ready For Pick Up"
        order.save()
        send_notification(order.user.admin.username, order.ref_code)
        return JsonResponse({'response':'success', 'message':'Order is ready for pick up!'})
    except Exception as e:
        print(e)
        return JsonResponse({'response':'error', 'message':'Please Try Again Later!!'})

@csrf_exempt
def set_complete(request):
    order_id = request.POST.get('id')
    order = Order.objects.get(id = order_id)

    try:
        order.delete()
        return JsonResponse({'response':'success', 'message':'Order is Complete!'})
    except Exception as e:
        return JsonResponse({'response':'error', 'message':'Please try again!'})

@csrf_exempt
def cancel_order(request):
    order_id = request.POST.get('id')
    order = Order.objects.get(id = order_id)
    item_obj = []
    for item in order.items.split(","):
        a = item.replace("(", "")
        a = a.replace(")", "")
        item_obj.append(a)

    try:
        for item in item_obj:
            a = item.split("x")
            product = Product.objects.get(name=a[1])
            product.stock = product.stock + int(a[0])
            product.save()
        order.delete()
        return JsonResponse({'response':'info', 'message':'Order has been canceled!'})
    except Exception as e:
        return JsonResponse({'response':'info', 'message':'Error!'})
