from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.orders.forms import CartAddForm
from apps.orders.models import Order, OrderItem
from apps.orders.services import Cart, OrderService
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


class OrderCreateView(View, LoginRequiredMixin):
    def get(self, request):
        cart = Cart.get_instance(request)
        order = Order.objects.create(user=request.user)

        OrderService.get_instance().create(cart, order)

        return redirect('orders:order_detail', order_id=order.id)


class OrderDetailView(View, LoginRequiredMixin):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        context = {
            'order': order
        }
        return render(request, 'orders/order.html', context)
