from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.products.models import Product
from apps.utils.base_model import BaseModel


class Order(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name='User')
    paid = models.BooleanField(default=False, verbose_name='Paid')
    coupon = models.ForeignKey('Coupon', null=True, blank=True, default=None, on_delete=models.PROTECT,
                               related_name='orders', verbose_name='Coupon')

    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.coupon:
            discount_price = (self.coupon.discount / 100) * total
            return int(total - discount_price)
        else:
            return total

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
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'


class Coupon(BaseModel):
    code = models.CharField(max_length=20, unique=True, verbose_name='Code')
    valid_from = models.DateTimeField(verbose_name='Valid from')
    valid_to = models.DateTimeField(verbose_name='Valid to')
    discount = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                verbose_name='Discount')
    active = models.BooleanField(default=False, verbose_name='Active')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        db_table = 'coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
