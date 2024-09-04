# Generated by Django 5.0.7 on 2024-09-04 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_sub',
            field=models.BooleanField(default=False, verbose_name='Is subcategory'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='products.category', verbose_name='Parent category'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='products.category', verbose_name='Category'),
        ),
    ]
