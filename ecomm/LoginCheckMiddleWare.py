from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user
        print(user.is_authenticated)
        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "ecomm.HODViews":
                    pass
                elif modulename == "ecomm.views" or modulename == "django.views.static":
                    pass
                else:
                    pass
                    #return redirect("add_school_year")

            elif user.user_type == "2":
                if modulename == "ecomm.StaffViews":
                    pass
                elif request.path == reverse("home"):
                    return redirect("staff_home")
                elif modulename == "ecomm.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("staff_home")

            elif user.user_type == "3":
                if modulename == "ecomm.CostumerViews":
                    pass
                elif request.path == reverse("home"):
                    return redirect("costumer_home")
                elif modulename == "ecomm.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("costumer_home")

            else:
                return redirect("home")

        else:
            if request.path == reverse("home") or request.path == reverse("doLogin"):
                pass
            else:
                return redirect("home")
