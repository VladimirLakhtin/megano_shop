# Generated by Django 4.2.4 on 2023-08-15 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tovar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('count', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=256)),
                ('fullDescription', models.TextField(blank=True)),
                ('freeDelivery', models.BooleanField(default=False)),
                ('is_banned', models.BooleanField(default=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tovari', to='catalog.category')),
                ('tags', models.ManyToManyField(blank=True, related_name='tagi', to='products.tag')),
            ],
        ),
    ]