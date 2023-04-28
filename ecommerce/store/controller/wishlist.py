from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Product, Cart, Wishlist
from django.contrib.auth.decorators import login_required


@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {"wishlist": wishlist}

    return render(request, 'store/wishlist.html', context)


def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if (product_check):
                if (Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({"status": 'Product Already in Wishlist'})
                else:
                    Wishlist.objects.create(
                        user=request.user, product_id=prod_id)
                    return JsonResponse({"status": 'Product Added Successfully'})
            else:
                return JsonResponse({"status": 'No Such a Product Found'})

        else:
            return JsonResponse({"status": 'Login To Continue'})
    return

def deletewishlistitem(request):
     if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))

            if (Wishlist.objects.filter(user=request.user,product_id=prod_id)):
                wishlist = Wishlist.objects.get(product_id=prod_id)
                wishlist.delete()
                return JsonResponse({"status":"Product Removed From WishList"})
            else:
                return JsonResponse({"status":"Product not found in wishlist"})
        else:
            return JsonResponse({"status": 'Login To Continue'})
     return redirect('/')