# Generated by Django 4.2.2 on 2023-07-27 10:11

import Shop.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0003_customer_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(default=1, upload_to=Shop.models.user_directory_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('disabled', 'Disabled'), ('draft', 'Drafts'), ('published', 'Published'), ('in_review', 'In Review')], max_length=10),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(2, '★★☆☆☆'), (1, '★✰✰✰✰'), (4, '★★★★☆'), (3, '★★★☆☆'), (5, '★★★★★')], default=None),
        ),
    ]
