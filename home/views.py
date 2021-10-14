from django.shortcuts import render
from .models import Popular_Products, For_You
from store.models import Product
    
def home(request):
    # popular_products = Popular_Products.objects.all().filter(is_available=True)
    products = Product.objects.all().filter(is_available=True)
    for_you = Product.objects.all().filter(is_available=True, new=False)
    new_products = Product.objects.all().filter(is_available=True, new=True)


    context = {
        #'popular_products': popular_products,
        'for_you':for_you,
        'new_products': new_products,
        'products':products,
    }
    return render(request, 'home/home.html', context)

