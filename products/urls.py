from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("blank/",views.blank,name='blank'),
    path("product/",views.listproduct,name='product'),
    path("productdetail/<int:product_id>/",views.detailproduct,name='productdetail'),
    


]