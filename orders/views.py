from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse

from cart.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from store.models import Product

import datetime
import json 


def place_order(request, total=0, quantity=0):
    current_user = request.user
    # if the cart cout less than 0 , redirect to store page 
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0 :
        return redirect('home:home')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    tax = round(((2 * total)/100), 2)
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.address2 = form.cleaned_data['address2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'tax': tax,
                'total': total,
                'grand_total' :grand_total,
            }
            return render(request, 'home/orders/checkout/payment.html', context)
        else:
            messages.error(request, 'Your information not Vailed')
            return redirect('cart:checkout')
            
    else:
        return redirect('store:store')


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    
    # Store transation details inside payment model 
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        status = body['status'],
        amount_paid = order.order_total,
    )
    
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    
    # Move the cart item to OrderProduct table 
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        # add variation to OrderProduct table
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        
        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Clear Cart 
    CartItem.objects.filter(user=request.user).delete()

    
    #Send order recieved email to cutomer 
    subject = 'Thank you for your order!'
    message = render_to_string('home/orders/checkout/payment_recieved_email.html', {
        'user': request.user,
        'order':order,
    })
    to_email = request.user.email
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()

    data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }
    return JsonResponse(data)
    


def order_completed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotall = 0
        for i in ordered_products:
            subtotall += i.product_price * i.quantity
        subtotal = round(subtotall, 2)
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'home/orders/checkout/order_completed.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store:store')
    