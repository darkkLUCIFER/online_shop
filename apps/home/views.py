import time

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from apps.home.tasks import get_all_bucket_objects_task, delete_object_task
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


class DeleteBucketObjectView(View):
    def get(self, request, key):
        delete_object_task.delay(key)
        messages.success(request, 'your object will be delete soon ', extra_tags='info')
        return redirect('home:bucket')
