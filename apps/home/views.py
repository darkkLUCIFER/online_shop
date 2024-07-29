from django.shortcuts import render
from django.views import View

from apps.products.models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        context = {
            'products': products
        }
        return render(request, 'home/home.html', context)
