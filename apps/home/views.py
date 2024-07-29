from django.shortcuts import render
from django.views import View

from apps.home.tasks import get_all_bucket_objects_task
from apps.products.models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        context = {
            'products': products
        }
        return render(request, 'home/home.html', context)


class BucketHomeView(View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = get_all_bucket_objects_task()
        context = {
            'objects': objects
        }
        return render(request, self.template_name, context)
