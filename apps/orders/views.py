from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.orders.forms import CartAddForm, CouponApplyForm
from apps.orders.models import Order
from apps.orders.services import Cart, OrderService, ZarinpalService, CouponService
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
    form_class = CouponApplyForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        context = {
            'order': order,
            'form': self.form_class()
        }
        return render(request, 'orders/order.html', context)


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)

        # save order in session
        request.session['order_pay'] = {
            'order_id': order.id
        }

        result = ZarinpalService.get_instance(request).set_amount(order.get_total_price()).send_request()
        if result['status']:
            url = result['url']
            return redirect(url)
        else:
            # todo: here you can save the error code for the order instance
            code = result['code']
            print(code)


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        result = ZarinpalService.get_instance(request).verify()
        if result['status']:
            ref_id = result['RefID']
            context = {
                'ref_id': ref_id
            }
        else:
            code = result['code']
            context = {
                'code': code
            }

        return render(request, 'orders/verify.html', context)


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code = cd['code']

            result = CouponService.get_instance().apply_coupon(code, order_id)
            if not result:
                messages.error(request, 'Coupon does not exist', extra_tags='danger')

            return redirect('orders:order_detail', order_id=order_id)
