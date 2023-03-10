from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Costumer"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name

class Costumer(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image= models.ImageField(upload_to='company')
    objects = models.Manager()

    def __str__(self):
        return self.name

class Motorcycle(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='motorcycle')
    anatomy_image = models.ImageField(upload_to='motorcycle_anatomy')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='motorcycle')
    objects = models.Manager()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product')
    price = models.FloatField()
    stock = models.IntegerField()
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"({self.quantity}x){self.item.name}-{self.item.motorcycle}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="Packaging")
    proccessed_by = models.ForeignKey(Staffs, on_delete=models.CASCADE, null=True)
    total = models.FloatField(default=0.0)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def split_order(self):
        return self.items.split(",")

class History(models.Model):
    user = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.name}"


class Transaction(models.Model):
    ref_code = models.CharField(max_length=255)
    costumer_name = models.CharField(max_length=255)
    cashier_name = models.CharField(max_length=255)
    item_list = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    total = models.CharField(max_length=255)

class UserLog(models.Model):
    transaction_id = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    cashier_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    logs = models.CharField(max_length=255)

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Costumer.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.costumer.save()
