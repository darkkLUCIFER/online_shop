from django.shortcuts import render, get_object_or_404
from django.views import View

from apps.products.models import Product


class ProductDetailView(View):
    form_class = 'products/detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        context = {
            'product': product
        }
        return render(request, self.form_class, context)
