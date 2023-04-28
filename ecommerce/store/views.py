from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import *
# Create your views here.


def home(request):
    trending_products = Product.objects.filter(trending=1)
    context = {'trending_products': trending_products}
    return render(request, 'store/index.html', context)


def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, 'store/collections.html', context)


def collectionsview(request, slug):
    if (Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'products': products, 'category': category}

        return render(request, "store/inc/indexx.html", context)
    else:
        messages.warning(request, "No Such Category Found.")
        return redirect('collections')


def productview(request, cate_slug, prod_slug):
    if (Category.objects.filter(slug=cate_slug, status=0)):
        if (Product.objects.filter(slug=prod_slug, status=0)):
            products = Product.objects.filter(slug=prod_slug, status=0).first()
            context = {'products': products}
        else:
            messages.error(request, 'No such product found')
            return redirect('collctions')
    else:
        messages.error(request, 'No such product found')
        return redirect('collctions')
    return render(request, 'store/inc/view.html', context)


def productlistajax(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productslist = list(products)
    return JsonResponse(productslist, safe=False)


def searchproducts(request):
    if request.method == "POST":
        searchterm = request.POST.get('productsearch')
        if searchterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchterm).first()

            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                messages.info(request, 'No Such Product Found')
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))
