from django.shortcuts import render, redirect
from .models import Product, Order

def product_list(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/product_list.html', {'products': products})

def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            product = Product.objects.get(id=product_id)
            request.session['cart'].append(product_id)
            request.session.modified = True

    cart_products = Product.objects.filter(id__in=request.session['cart'])
    return render(request, 'ecommerce/cart.html', {'cart_products': cart_products})

def pay_now(request):
    if 'cart' in request.session:
        cart_product_ids = request.session['cart']
        products = Product.objects.filter(id__in=cart_product_ids)

        # Create the order
        order = Order.objects.create()
        order.products.set(products)

        # Clear the cart
        del request.session['cart']

        return render(request, 'ecommerce/pay_now.html', {'order': order})

    return redirect('cart')

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'ecommerce/order_list.html', {'orders': orders})
