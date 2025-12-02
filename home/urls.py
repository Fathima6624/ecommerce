from django.urls import path

from . import views

urlpatterns = [

path("contact/",views.contact,name="contact"),
path("privacy",views.privacy,name="privacy"),
path("returnpolicy",views.returnpolicy,name="returnpolicy"),
path("faq",views.faq,name="faq"),
path("readmore",views.readmore,name="readmore")

]