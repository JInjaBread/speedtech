import json
import pandas as pd
from io import BytesIO
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import *
from django.views import View
from xhtml2pdf import pisa

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def admin_home(request):
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
    return render(request, 'adminHOD/admin_home.html', context)

def company(request):
    company = Company.objects.all()

    context = {
        "company": company
    }
    return render(request, 'adminHOD/company.html', context)

def add_company(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_home')
    else:
        name = request.POST.get("name")

        if len(request.FILES) != 0:
            image_file = request.FILES['file']
        else:
            image_file = None

        try:
            company = Company(name=name, image=image_file)
            company.save()
            messages.success(request, "Company saved Succesfully")
            return redirect('admin_company')
        except Exception as e:
            print(e)
            messages.error(request,"Failed to save")
            return redirect('admin_company')

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
                return redirect('admin_company')
            except:
                messages.error(request, "Error on Submit")
                return redirect('admin_company')
        else:
            try:
                company.name = name
                company.image = image_file
                company.save()
                messages.success(request, "Saved Succesfully")
                return redirect('admin_company')
            except:
                messages.error(request, "Error on Submit")
                return redirect('admin_company')

def delete_company(request, company_id):
    company = Company.objects.get(id=company_id)

    try:
        company.delete()
        messages.success(request, "Deleted Succesfully")
        return redirect('admin_company')
    except Exception as e:
        print(e)
        messages.error(request, "Error on Submit")
        return redirect('admin_company')

def motorcycle(request):
    company = Company.objects.all()
    motorcycle = Motorcycle.objects.all()
    context = {
        "motorcycle": motorcycle,
        "company": company
    }
    return render(request, 'adminHOD/motorcycle.html', context)

def add_motorcycle(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('admin_motorcycle')
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
        return redirect('admin_motorcycle')
    except:
        messages.error(request, "Motorcycle Save Unsucessfull")
        return redirect('admin_motorcycle')

def edit_motorcycle(request, motorcycle_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('admin_motorcycle')
    else:
        motorcycle = Motorcycle.objects.get(id=motorcycle_id)
        name = request.POST.get('name')
        company = request.POST.get('company')
        company_obj = Company.objects.get(id=company)
        anatomy_check = request.POST.get('anatomy')
        image_check = request.POST.get('file')

        if image_check != "":
            image_file = request.FILES['file']
        else:
            image_file = None

        if anatomy_check != "":
            anatomy_image = request.FILES['anatomy']
        else:
            anatomy_image = None


        if image_file == None:
            try:
                motorcycle.name = name
                motorcycle.company = company_obj
                motorcycle.anatomy_image = anatomy_image
                motorcycle.save()
                messages.success(request, "Saved Succesfully")
                return redirect('admin_motorcycle')
            except:
                messages.error(request, "Error on Submit")
                return redirect('admin_motorcycle')

        elif anatomy_image == None:
            try:
                motorcycle.name = name
                motorcycle.company = company_obj
                motorcycle.image = image_file
                motorcycle.save()
                messages.success(request, "Saved Succesfully")
                return redirect('admin_motorcycle')
            except:
                messages.error(request, "Error on Submit")
                return redirect('admin_motorcycle')
        elif image_file != None and anatomy_image != None:
            try:
                motorcycle.name = name
                motorcycle.company = company_obj
                motorcycle.anatomy_image = anatomy_image
                motorcycle.image = image_file
                motorcycle.save()
                messages.success(request, "Saved Succesfully")
                return redirect('admin_motorcycle')
            except:
                messages.error(request, "Error on Submit")
                return redirect('admin_motorcycle')
        else:
            try:
                motorcycle.name = name
                motorcycle.company = company_obj
                motorcycle.save()
                messages.success(request, "Saved Succesfully")
                return redirect('admin_motorcycle')
            except:
                messages.error(request, "Error on Submit")
                return redirect('admin_motorcycle')

def delete_motorcycle(request, motorcycle_id):
    motorcycle = Motorcycle.objects.get(id=motorcycle_id)

    try:
        motorcycle.delete()
        messages.success(request, "Deleted Succesfully")
        return redirect('admin_motorcycle')
    except:
        messages.error(request, "Error on Submit")
        return redirect('admin_motorcycle')

def products(request):
    motorcycle = Motorcycle.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "motorcycle": motorcycle
    }
    return render(request, 'adminHOD/products.html', context)

def admin_add_products(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('admin_products')
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
            return redirect('admin_products')
        except Exception as e:
            print(e)
            messages.success(request, "Error Saving Products")
            return redirect('admin_products')

def admin_edit_products(request, product_id):
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
                return redirect('admin_products')
            except Exception as e:
                print(e)
                messages.error(request, "Error on Submit")
                return redirect('admin_products')
        else:
            try:
                product.name = name
                product.price = price
                product.stock = stock
                product.motorcycle = motorcycle
                product.category = category
                product.image = image_file
                product.save()
                messages.success(request, "Saved Succesfully")
                return redirect('admin_products')
            except Exception as e:
                print(e)
                messages.error(request, "Error on Submit")
                return redirect('admin_products')

def delete_products(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        product.delete()
        messages.success(request, "Deleted Succesfully")
        return redirect('admin_products')
    except:
        messages.error(request, "Error on Submit")
        return redirect('admin_products')

def admin_account(request):
    users_obj = Staff.objects.all()

    context = {
        "users_obj": users_obj,
    }
    return render(request, 'adminHOD/account.html', context)

def transaction(request):
    return render(request, 'adminHOD/transaction.html')

@csrf_exempt
def get_transaction(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    date_index = pd.date_range(start=start_date, end=end_date)
    transaction_data = []
    try:
        for date in date_index:
            print(date)
            transaction_obj = Transaction.objects.filter(date=date)
            for transaction in transaction_obj:
                transaction_temp = Transaction.objects.get(id=transaction.id)
                data_small = {"id": transaction.id, "costumer_name":transaction.costumer_name, "cashier_name":transaction.cashier_name, "item_list":transaction.item_list, "date":str(transaction.date), "total":transaction.total}
                transaction_data.append(data_small)
    except Exception as e:
        print("error")

    return JsonResponse(json.dumps(transaction_data, cls=DecimalEncoder), content_type="application/json", safe=False)

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        d = request.session['data']
        pdf = render_to_pdf('adminHOD/pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

def staff(request):
    staffs = Staffs.objects.all()

    context= {
        'staffs':staffs
    }

    return render(request, 'adminHOD/staff.html', context)

@csrf_exempt
def get_staff(request):
    staffs = Staffs.objects.all()
    print(staffs)
    data = []
    for staff in staffs:
        data_small = {'id':staff.id, 'first_name': staff.admin.first_name, 'last_name':staff.admin.last_name, 'last_login': str(staff.admin.last_login), 'address':staff.address}
        data.append(data_small)

    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)

def add_staff(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    address = request.POST.get('address')
    try:
        user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, user_type=2)
        user.staffs.address = address
        user.save()
        messages.success(request, "Success")
        return redirect('staff')
    except:
        messages.error(request, "Error on Submit")
        return redirect('staff')

def edit_staff(request, staff_id):
    staff = Staffs.objects.get(id = staff_id)
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    address = request.POST.get('address')

    try:
        if password != None:
            staff.admin.first_name = first_name
            staff.admin.last_name = last_name
            staff.admin.username = username
            staff.admin.password = password
            staff.address = address
            staff.save()
            messages.success(request, "Success")
            return redirect('staff')
        else:
            staff.admin.first_name = first_name
            staff.admin.last_name = last_name
            staff.admin.username = username
            staff.address = address
            messages.success(request, "Success")
            return redirect('staff')
    except:
        messages.error(request, "Error on Submit")
        return redirect('staff')

def delete_staff(request, staff_id):
    staff = Staffs.objects.get(id=staff_id)
    user = CustomUser.objects.get(id=staff.admin.id)
    try:
        staff.delete()
        user.delete()
        messages.success(request, "Deleted Succesfully")
        return redirect('staff')
    except:
        messages.error(request, "Error on Submit")
        return redirect('staff')
