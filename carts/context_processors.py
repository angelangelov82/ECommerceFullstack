from .models import Cart, CartItem
from .views import _cart_id

def counter(request): # function counter
    cart_count = 0
    if 'admin' in request.path: # first handleing for admin
        return {}               # when logged in as admin, should not see anything in the cart
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request)) #get the cart
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user) #get cart items filtert by the cart with one result
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1]) #get cart items filtert by the cart with one result
            for cart_item in cart_items: # get the quantity of items in the cart
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)
