# Generated by Django 5.1.6 on 2025-03-04 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_contactadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactadmin',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
