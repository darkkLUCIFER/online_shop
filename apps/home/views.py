import os
import time

from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.views import View

from apps.home.forms import UploadBucketObjectForm
from apps.home.tasks import get_all_bucket_objects_task, delete_object_task, download_object_task, upload_object_task
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
    form_class = UploadBucketObjectForm

    def get(self, request):
        objects = get_all_bucket_objects_task()
        context = {
            'objects': objects
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            temp_file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            upload_object_task.delay(temp_file_path)
            messages.success(request, 'your object will be upload soon ', extra_tags='info')
        else:
            messages.error(request, 'Invalid Credentials', extra_tags='error')

        return redirect('home:bucket')


class DeleteBucketObjectView(View):
    def get(self, request, key):
        delete_object_task.delay(key)
        messages.success(request, 'your object will be delete soon ', extra_tags='info')
        return redirect('home:bucket')


class DownloadBucketObjectView(View):
    def get(self, request, key):
        download_object_task.delay(key)
        messages.success(request, 'your object will be download soon ', extra_tags='info')
        return redirect('home:bucket')
