# Generated by Django 5.0.4 on 2024-05-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default='Abuja', max_length=200),
        ),
    ]