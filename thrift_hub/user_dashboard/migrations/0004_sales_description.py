# Generated by Django 5.0.4 on 2024-04-26 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard', '0003_gallerymedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='description',
            field=models.TextField(default='NULL'),
        ),
    ]
