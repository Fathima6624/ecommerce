from django.shortcuts import render,redirect
from django.contrib import messages

# Create your views here.

from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        messages.success(request, "Thank you! Your message has been sent successfully.")
        return redirect("contact")

    return render(request, "contact.html")





def privacy(request):
    return render(request,"privacypolicy.html")




def returnpolicy(request):
    return render(request,"returnpolicy.html")


def faq(request):
    return render(request,"faq.html")


def readmore(request):
    return render(request,"readmore.html")










