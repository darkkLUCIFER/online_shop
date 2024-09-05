from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from apps.orders.forms import CartAddForm
from apps.orders.services import Cart
from apps.products.models import Product


class CartView(View):
    def get(self, request):
        cart = Cart.get_instance(request)

        context = {
            'cart': cart
        }
        return render(request, 'orders/cart.html', context)


class CartAddView(View):
    form_class = CartAddForm

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            quantity = cd["quantity"]

            # add product to user cart
            Cart.get_instance(request).add(product, quantity)

        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart.get_instance(request)
        product = get_object_or_404(Product, pk=product_id)
        cart.remove(product)
        return redirect('orders:cart')
