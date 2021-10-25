from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Product, Category
from cart.models import CartItem
from cart.views import _cart_id

def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()



    context = {
        'category_slug':category_slug,
        'products':paged_products ,
        'products_count': products_count,
    }

    return render(request, "home/store/store.html", context)

def product_details(request, category_slug, product_details_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_details_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        return e
    
    
    context ={
        'single_product': single_product,
        'in_cart': in_cart,
    }

    return render(request, 'home/store/product_details.html', context)

def search(request):
    products_count = 0
    products = None
    paged_products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword :
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            
            products_count = products.count()
            
    
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, "home/store/store.html", context)