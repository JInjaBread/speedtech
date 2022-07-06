from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	path('login', views.loginpage, name="login"),
	path('doLogin', views.doLogin, name="doLogin"),
	path('logout_user', views.logout_user, name="logout_user"),
	path('signup', views.signup, name="signup"),
	path('verify_otp', views.verify_otp, name="verify_otp"),
	path('motorcycle', views.motorcycle, name="motorcycle"),
	path('motorcycle_company/<company_id>', views.motorcycle_company, name="motorcycle_company"),
	path('product', views.product, name="product"),
	path('product/<category_id>', views.product_category, name="product_category"),
	path('cart', views.cart, name="cart"),
	path('add_to_cart/<product_id>', views.add_to_cart, name="add_to_cart"),
	path('update_cart/<item_id>', views.update_cart, name="update_cart"),
	path('remove_from_cart/<item_id>', views.remove_from_cart, name="remove_from_cart"),
	path('order', views.order, name="order"),
	path('make_order', views.make_order, name="make_order"),
]
