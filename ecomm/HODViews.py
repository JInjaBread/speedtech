from django.shortcuts import render, redirect

def admin_home(request):
    order = Order.objects.all()
    order_obj = []
    for order in order:
        print(order.ref_code)
        if order.ref_code != None:
            order_obj.append(order)

    staff = []
    costumer = []

    user = CustomUser.objects.all()

    for user in user:
        if user.user_type == "2":
            staff.append(user)
        else if user.user_type == "3":
            costumer.append(user)
    context = {
        "order": order,
        "staff": staff,
        "costumer": costumer,
    }
    return render(request, 'adminHOD/admin_home.html')

def company(request):
    company = Company.objects.all()

    context = {
        "company": company
    }
    return render(request, 'adminHOD/company.html')

def add_company(request):
    if request.method == "POST":
        mesages.error(request, "Invalid Method!")
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
        except Exception as e:
            print(e)
            messages.error(request,"failed to save")
            return redirect('company')
