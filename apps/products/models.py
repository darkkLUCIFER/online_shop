from django.db import models
from django.urls import reverse

from apps.utils.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=200, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    active = models.BooleanField(default=True, verbose_name='Active')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'category'
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Category')
    name = models.CharField(max_length=200, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Image')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    price = models.IntegerField(verbose_name='Price')
    available = models.BooleanField(verbose_name='Available', default=True)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name} - {self.category}'

    class Meta:
        db_table = 'product'
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
