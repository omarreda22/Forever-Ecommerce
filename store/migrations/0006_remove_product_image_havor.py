# Generated by Django 3.2.3 on 2021-11-05 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_reviewrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_havor',
        ),
    ]
