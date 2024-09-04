from django.shortcuts import render, get_object_or_404
from django.views import View

from apps.orders.forms import CartAddForm
from apps.products.models import Product


class ProductDetailView(View):
    template_name = 'products/detail.html'
    form_class = CartAddForm

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        context = {
            'product': product,
            'add_to_cart_form': self.form_class
        }
        return render(request, self.template_name, context)
