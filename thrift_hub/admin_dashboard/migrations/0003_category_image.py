# Generated by Django 5.0.4 on 2024-05-15 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0002_rename_name_category_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='category_images/'),
        ),
    ]
