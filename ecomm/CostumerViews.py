import random, string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

def costumer_home(request):
    user = Costumer.objects.get(admin=request.user)
    cart = OrderItem.objects.filter(user_id=user.id)
    company = Company.objects.all()
    all_motorcycle = Motorcycle.objects.all()
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
    products = Product.objects.filter(motorcycle = motorcycle)
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

    order_qs = OrderItem.objects.filter(user=user.id, ordered=False)
    if order_qs.exists():
        order = order_qs.filter(item = product)
        if order.exists():
            messages.info(request, "Item is allready in the cart!.")
            return redirect(request.META['HTTP_REFERER'])
        else:
            order_item, created = OrderItem.objects.get_or_create(
                item=product,
                user=user,
                ordered=False
            )
            messages.info(request, "Item added to cart!!")
            return redirect(request.META['HTTP_REFERER'])
    else:
        cart = OrderItem(
            item=product,
            user=user,
            ordered=False
        )
        cart.save()
        messages.info(request, "Item added to cart!.")
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
