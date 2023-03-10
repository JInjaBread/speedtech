import random, string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q

def costumer_home(request):

    if 'search' in request.GET:
        search = request.GET['search']
        all_motorcycle = Motorcycle.objects.filter(name__icontains=search)
    else:
        all_motorcycle = Motorcycle.objects.all()
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    company = Company.objects.all()
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
        "company": company,
        "cart":cart,
        "all_motorcycle": all_motorcycle,
        "order_count": order_count,
        "order": order,
    }
    return render(request, 'costumer/costumer_home.html', context)

def cart(request):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
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
            "order_count":order_count
        }

    return render(request, 'costumer/cart.html', context)

def motorcycle(request, motorcycle_name):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    motorcycle = Motorcycle.objects.get(name = motorcycle_name)
    category = Category.objects.all()
    product = Product.objects.filter(motorcycle = motorcycle)
    if 'search' in request.GET:
        search = request.GET['search']
        products = product.filter(name__icontains=search)
    else:
        products = product
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
        "category": category,
        "products": products,
        "cart":cart,
        "order_count": order_count,
        "order": order,
    }

    return render(request, 'costumer/costumer_products_view.html', context)

def update_cart(request, item_id):
    quantity = request.POST.get('quantity')
    print(quantity)
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    cart_to_update = cart.get(id=item_id)
    product = Product.objects.get(id=cart_to_update.item.id)
    if quantity != '0':
        if int(quantity) > product.stock:
            messages.error(request, "Quantity Error")
            return redirect(request.META['HTTP_REFERER'])
        else:
            try:
                cart_to_update.quantity = quantity
                cart_to_update.save()
                messages.info(request, "Item was updated")
                return redirect(request.META['HTTP_REFERER'])
            except:
                messages.info(request, "Error on Request!.")
                return redirect(request.META['HTTP_REFERER'])

@csrf_exempt
def add_to_cart(request):
    product_id = request.POST.get('id')
    product = get_object_or_404(Product, id=product_id)
    user = Costumer.objects.get(admin=request.user)

    order_qs = OrderItem.objects.filter(user=user.id, ordered=False)
    if order_qs.exists():
        order = order_qs.filter(item = product)
        if order.exists():
            return JsonResponse({'response':'info', 'message':'Item is allready in the cart'})
        else:
            order_item, created = OrderItem.objects.get_or_create(
                item=product,
                user=user,
                ordered=False
            )
            return JsonResponse({'response':'success', 'message':'Item added to the cart'})
    else:
        cart = OrderItem(
            item=product,
            user=user,
            ordered=False
        )
        cart.save()
        return JsonResponse({'response':'success', 'message':'Item added to cart!'})

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

def order(request):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
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
        "user":user,
        "cart":cart,
        "order_obj":order_obj,
        "order_count": order_count,
    }
    return render(request, 'costumer/que_order.html', context)

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

@csrf_exempt
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
            list = list + ", " +str(item)
            history = History(user=user, item=item.item)
            product = Product.objects.get(id=item.item.id)
            product.stock = product.stock - item.quantity
            history.save()
            product.save()
            item.delete()
        list = list[1:]
        order.items = list
        history.save()
        order.save()
        return JsonResponse({'response':'success', 'message':'Order Success!'})
    except Exception as e:
        print(e)
        return JsonResponse({'response':'error', 'message':'Order Success!'})

def search_result(request, search):
    cont = Q(name__icontains=search)
    motorcycle = Motorcycle.objects.filter(name=cont)
    products = Product.objects.filter(name=cont)
    context = {
        'motorcycle': motorcycle,
        'products': products
    }
    return render(request, 'costumer/costumer_search_view.html', context)

def history(request):
    user = Costumer.objects.get(admin=request.user)
    products = []
    history = History.objects.filter(user=user)
    for history in history:
        if history.item not in products:
            products.append(history.item)
        else:
            pass
    context = {
    'products': products
    }
    return render(request, 'costumer/history.html', context)
