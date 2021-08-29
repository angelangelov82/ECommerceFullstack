from django.shortcuts import render
from store.models import Product, ReviewRaiting


def home(request):
    products = Product.objects.all().filter(is_available=True). order_by('created_date')# bring all available products
    #Get the reviews
    for product in products:
        reviews = ReviewRaiting.objects.filter(product_id=product.id, status=True)
    context ={
        'products': products,
        'reviews': reviews
    }
    return render(request, 'home.html', context)
