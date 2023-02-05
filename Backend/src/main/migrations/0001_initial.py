# Generated by Django 4.1.6 on 2023-02-04 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Description')),
                ('thumbnail', models.ImageField(upload_to='categories')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='Amount')),
                ('unit', models.CharField(max_length=64, verbose_name='Unit')),
            ],
            options={
                'verbose_name': 'measure',
                'verbose_name_plural': 'measures',
                'ordering': ('unit',),
                'unique_together': {('amount', 'unit')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
                ('thumbnail', models.ImageField(upload_to='products')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
                ('instructions', models.TextField(verbose_name='Instructions')),
                ('thumbnail', models.ImageField(upload_to='receipts')),
                ('youtube_link', models.CharField(blank=True, max_length=256, null=True, verbose_name='YouTube link')),
                ('source', models.CharField(blank=True, max_length=256, null=True, verbose_name='Source link')),
                ('date_created', models.DateTimeField(auto_now=True, verbose_name='Date created')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.area')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('measures', models.ManyToManyField(to='main.measure')),
                ('products', models.ManyToManyField(to='main.product')),
                ('tags', models.ManyToManyField(to='main.tag')),
            ],
            options={
                'verbose_name': 'receipt',
                'verbose_name_plural': 'receipts',
                'ordering': ('name',),
            },
        ),
    ]
