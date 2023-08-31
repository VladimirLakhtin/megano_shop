# Generated by Django 4.2.4 on 2023-08-15 12:37

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='categoryimage',
            name='src',
            field=models.ImageField(upload_to=catalog.models.get_category_image_path, verbose_name='Ссылка'),
        ),
    ]
