from django.urls import path

from . import views
from . import CostumerViews, StaffViews
urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	#path('login', views.loginpage, name="login"),
	path('doLogin', views.doLogin, name="doLogin"),
	path('logout_user', views.logout_user, name="logout_user"),
	path('signup', views.signup, name="signup"),
	path('verify_otp', views.verify_otp, name="verify_otp"),

	#path for costumer
	path('costumer_home', CostumerViews.costumer_home, name="costumer_home"),
	path('costumer_home/<motorcycle_name>', CostumerViews.motorcycle, name="motorcycle"),
	#path('product', views.product, name="product"),
	#path('product/<category_id>', views.product_category, name="product_category"),
	path('cart', CostumerViews.cart, name="cart"),
	path('add_to_cart/<product_id>', CostumerViews.add_to_cart, name="add_to_cart"),
	path('update_cart/<item_id>', CostumerViews.update_cart, name="update_cart"),
	path('remove_from_cart/<item_id>', CostumerViews.remove_from_cart, name="remove_from_cart"),
	path('order', CostumerViews.order, name="order"),
	path('make_order', CostumerViews.make_order, name="make_order"),

	#path for staffs
	path('staff_home', StaffViews.staff_home, name="staff_home"),
	path('costumer', StaffViews.costumer, name="costumer"),
	path('company', StaffViews.company, name="company"),
	path('add_company', StaffViews.add_company, name="add_company"),
	path('edit_company/<company_id>', StaffViews.edit_company, name="edit_company"),
	path('motorcycle', StaffViews.motorcycle, name="motorcycle"),
	path('products', StaffViews.products, name="products"),
	path('save_products', StaffViews.save_products, name="save_products"),
	path('orders', StaffViews.orders, name="orders"),
	path('set_ready/<order_id>', StaffViews.set_ready, name="set_ready"),
	path('set_complete/<order_id>', StaffViews.set_complete, name="set_complete"),
	path('cancel_order/<order_id>', StaffViews.cancel_order, name="cancel_order"),
]
