# Generated by Django 5.0.4 on 2024-04-26 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0004_sales_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='description',
            field=models.TextField(default='No description'),
        ),
    ]
