from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request): # private function to get the session id that will be the cart id:
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id): #create cart VIDEO &% explan
    current_user = request.user
    product = Product.objects.get(id=product_id) # get the product id from Store Product class - get the product

    if current_user.is_authenticated: # if statement for aouthenticatin an handling the add cart in differend cases
        product_variation = [] #store product variations in empty list - get the product variation here
        if request.method == 'POST': #check is the request is post
            for item in request.POST: # loop trough any value that is comming from the post request
                key = item
                value = request.POST[key]

                try: #check key and value came from the post request maching the variation values
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value) #get the variation here
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists: # if cart item exist statement for handling the existed cart items in differend cases
            cart_item = CartItem.objects.filter(product = product, user=current_user)
            existing_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in existing_var_list:
                index = existing_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id = item_id)
                item.quantity +=1 #increase the cart item quantity
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) >0: # check if the product variation list is empty or not
                    item.variations.clear() # clear the variations choices from cart_items variations:
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user,
            )
            if len(product_variation) >0:  # add the product variation in the cart item
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    else:
        product_variation = [] #store product variations in empty list - get the product variation here
        if request.method == 'POST': #check is the request is post
            for item in request.POST: # loop trough any value that is comming from the post request
                key = item
                value = request.POST[key]

                try: #check key and value came from the post request maching the variation values
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value) #get the variation here
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request)) # get the cart using the cart id from the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            ) #if the cart does not exist create it
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product = product, cart=cart) # create a new cart item every time a cart item is added to the cart
            #if current variations is in existing variations then increase the quantity of the cart_itm if a product with a variation is selected twise
            existing_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                existing_var_list.append(list(existing_variation))
                id.append(item.id)

            print(existing_var_list)

            if product_variation in existing_var_list:
                index = existing_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id = item_id)
                item.quantity +=1 #increase the cart item quantity
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) >0: # check if the product variation list is empty or not
                    item.variations.clear() # clear the variations choices from cart_items variations:
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) >0:  # add the product variation in the cart item
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

def remove_cart(request, product_id, cart_item_id): # decrement items from the cart page
    product = get_object_or_404(Product, id = product_id) # get the product
    try:
        if request.user.is_authenticated: # if the user is logged in
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:# if the user is logged in
            cart = Cart.objects.get(cart_id=_cart_id(request))# get the carts
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get cart items
        if cart_item.quantity > 1: #if more than 1 product in the cart
            cart_item.quantity -= 1# remove 1 item
            cart_item.save()
        else:
            cart_item.delete()# if only one product in the cart, delete it
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id = product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated: # this is for logged in users
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else: # this is for not logged users
            cart = Cart.objects.get(cart_id=_cart_id(request)) # taking the cart object by cart id
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) # taking the cart items
        for cart_item in cart_items:                                    # looking for cart items
            total += (cart_item.product.price * cart_item.quantity)     # to get total of each cart item
            quantity += cart_item.quantity                              #and the quantity
        tax = (2 * total)/100 # tax is evaluated as 2% for this project
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = { #sending the context to cart.html file
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context) # define cart url

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated: # this is for logged in users
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else: # this is for not logged users
            cart = Cart.objects.get(cart_id=_cart_id(request)) # taking the cart object by cart id
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) # taking the cart items
        for cart_item in cart_items:                                    # looking for cart items
            total += (cart_item.product.price * cart_item.quantity)     # to get total of each cart item
            quantity += cart_item.quantity                              #and the quantity
        tax = (2 * total)/100 # tax is evaluated as 2% for this project
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = { #sending the context to cart.html file
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
