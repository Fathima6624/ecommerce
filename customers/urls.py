from django.urls import path
from . import views

urlpatterns = [
    path("index/",views.index,name="index"),
    path("register/",views.register,name="register"),
    path("login/",views.loginform,name="login"),
    path("logout/",views.log_out,name="logout"),

]