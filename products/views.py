from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

from . models import Product

from django.core.paginator import Paginator
# Create your views here.



def index(request):
    products = Product.objects.all()[:8]  # show 8 products on home page
    return render(request, 'index.html', {'products': products})


def blank(request):
    return render(request,"blank.html")



def listproduct(request):
    products = Product.objects.all()

    paginator = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,   # important: pass page_obj instead of products
    }

    return render(request, "product.html", context)




@login_required
def detailproduct(request, product_id):
    product = get_object_or_404(Product, id=product_id, delete_status=1)
    return render(request, "product-detail.html", {"product": product})


