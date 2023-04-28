from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Product, Cart, Wishlist, Order, OrderItem, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse
import random


@login_required(login_url='loginpage')
def index(request):
    rowcart = Cart.objects.filter(user=request.user)
    for item in rowcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)
    cartitem = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitem:
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()

    context = {'cartitem': cartitem,
               'total_price': total_price, 'userprofile': userprofile}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':
        # below code is for auto filling checkout form
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        # this code is for saving checkout incoming data
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + \
                item.product.selling_price * item.product_qty
        neworder.total_price = cart_total_price

        trackno = 'soni'+str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno):
            trackno = 'soni'+str(random.randint(1111111, 9999999))
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            # To decrease the product quanity from avalable stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

            # To clear users cart
            Cart.objects.filter(user=request.user).delete()
            messages.success(request, "Congratulations! Your Order is Placed")

            PayMode = request.POST.get('payment_mode')
            if (PayMode == "Paid By RazorPay" or PayMode == "Paid By PayPal"):
                return JsonResponse({'status': 'Congratulations! Your Order is Placed'})
            else:
                return messages(request, "Your Order Has been Placed Successfully")

    return redirect('/')


@login_required(login_url='loginpage')
def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price+item.product.selling_price * item.product_qty

    return JsonResponse(
        {"total_price": total_price}
    )
