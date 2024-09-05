from django.contrib.auth import get_user_model
from django.db import models

from apps.products.models import Product
from apps.utils.base_model import BaseModel


class Order(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name='User')
    paid = models.BooleanField(default=False, verbose_name='Paid')

    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        db_table = 'orders'
        ordering = ('paid', '-updated_at')
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Product')
    price = models.PositiveIntegerField(verbose_name='Price')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')

    def __str__(self):
        return self.id

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'
