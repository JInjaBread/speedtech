from django.urls import path

from . import views
from . import CostumerViews, StaffViews, HODViews

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	#path('login', views.loginpage, name="login"),
	path('doLogin', views.doLogin, name="doLogin"),
	path('logout_user', views.logout_user, name="logout_user"),
	path('signup', views.signup, name="signup"),
	path('verify_otp', views.verify_otp, name="verify_otp"),
	path('forgot_password', views.forgot_password, name="forgot_password"),
	path('send', views.send, name="send"),
	path('verify_otp_reset', views.verify_otp_reset, name="verify_otp_reset"),
	path('reset_password', views.reset_password, name="reset_password"),
	path('check_phone_exist', views.check_phone_exist, name="check_phone_exist"),

	#path for admin
	path('admin_home', HODViews.admin_home, name="admin_home"),
	path('admin_company', HODViews.company, name="admin_company"),
	path('admin_add_company', HODViews.add_company, name="admin_add_company"),
	path('admin_edit_company/<company_id>', HODViews.edit_company, name="admin_edit_company"),
	path('delete_company', HODViews.delete_company, name="delete_company"),
	path('admin_motorcycle', HODViews.motorcycle, name="admin_motorcycle"),
	path('admin_add_motorcycle', HODViews.add_motorcycle, name="admin_add_motorcycle"),
	path('admin_edit_motorcycle/<motorcycle_id>', HODViews.edit_motorcycle, name="admin_edit_motorcycle"),
	path('delete_motorcycle', HODViews.delete_motorcycle, name="delete_motorcycle"),
	path('admin_products', HODViews.products, name="admin_products"),
	path('admin_add_products', HODViews.admin_add_products, name="admin_add_products"),
	path('admin_edit_products/<product_id>', HODViews.admin_edit_products, name="admin_edit_products"),
	path('delete_products', HODViews.delete_products, name="delete_products"),
	path('transaction', HODViews.transaction, name="transaction"),
	path('get_transaction', HODViews.get_transaction, name="get_transaction"),
	path('staff/', HODViews.staff, name="staff"),
	path('get_staff/', HODViews.get_staff, name="get_staff"),
	path('add_staff/', HODViews.add_staff, name="add_staff"),
	path('edit_staff/<staff_id>', HODViews.edit_staff, name="edit_staff"),
	path('staff/delete_staff/<staff_id>', HODViews.delete_staff, name="delete_staff"),
	path('get_sales/', HODViews.get_sales, name="get_sales"),
	path('categories/', HODViews.categories, name="categories"),
	path('add_category/', HODViews.add_category, name="add_category"),
	path('edit_category/<category_id>', HODViews.edit_category, name="edit_category"),
	path('delete_category/', HODViews.delete_category, name="delete_category"),

	#path for costumer
	path('costumer_home', CostumerViews.costumer_home, name="costumer_home"),
	path('costumer_home/<motorcycle_name>', CostumerViews.motorcycle, name="motorcycle"),
	#path('product', views.product, name="product"),
	#path('product/<category_id>', views.product_category, name="product_category"),
	path('cart', CostumerViews.cart, name="cart"),
	path('add_to_cart', CostumerViews.add_to_cart, name="add_to_cart"),
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
	path('add_motorcycle', StaffViews.add_motorcycle, name="add_motorcycle"),
	path('products', StaffViews.products, name="products"),
	path('save_products', StaffViews.save_products, name="save_products"),
	path('edit_product/<product_id>', StaffViews.edit_product, name="edit_product"),
	path('orders', StaffViews.orders, name="orders"),
	path('get_orders', StaffViews.get_orders, name="get_orders"),
	path('get_orders_data', StaffViews.get_orders_data, name="get_orders_data"),
	path('set_ready', StaffViews.set_ready, name="set_ready"),
	path('set_complete', StaffViews.set_complete, name="set_complete"),
	path('cancel_order', StaffViews.cancel_order, name="cancel_order"),

]
