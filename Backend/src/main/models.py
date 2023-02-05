from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
import os


class Category(models.Model):
    """Categories for Products"""
    slug = models.SlugField(_("Slug"), max_length=256, unique=True, blank=True)
    name = models.CharField(_("Name"), max_length=256, unique=True)
    description = models.CharField(_("Description"), max_length=1024, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='categories')

    def get_absolute_url(self):
        return reverse("category_receipts", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.description.strip():
            self.description = 'Without description'
        self.slug = slugify(self.name)
        self.thumbnail.name = self.slug + '.jpg'
        thumbnail_path = settings.BASE_DIR / f"media/categories/{self.thumbnail.name}"
        method = kwargs.pop('method') if kwargs.get('method', None) is not None else 'create'
        if os.path.exists(thumbnail_path) and method == 'create':
            os.remove(thumbnail_path)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        description = ' '.join(self.description.split()[:30] + ['...']) if len(self.description.split()) > 30 else self.description
        return f"{self.name}"


class Area(models.Model):
    """Areas for Receipts"""
    name = models.CharField(_("Name"), max_length=256, unique=True)

    def save(self, *args, **kwargs):
        if self.name.lower().strip() in ('russia', 'russian',):
            self.name = 'Ukrainian'
        super(Area, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    def __str__(self):
        return f"{self.name}"


class Measure(models.Model):
    """Measures for Receipts"""
    amount = models.PositiveIntegerField(_("Amount"))
    unit = models.CharField(_("Unit"), max_length=64)

    class Meta:
        unique_together = ('amount', 'unit',)
        ordering = ('unit',)
        verbose_name = _('measure')
        verbose_name_plural = _('measures')

    def __str__(self):
        return f"{self.amount} {self.unit}"


class Tag(models.Model):
    """Tag for Receipts"""
    name = models.CharField(_("Tag"), max_length=64, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """User's Products for Receipts"""
    slug = models.SlugField(_("Slug"), max_length=256, unique=True, blank=True)
    name = models.CharField(_("Name"), max_length=256, unique=True)
    thumbnail = models.ImageField(upload_to='products')
    description = models.TextField(_("Description"), null=True, blank=True)

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.description.strip():
            self.description = 'Without description'
        self.slug = slugify(self.name)
        self.thumbnail.name = self.slug + '.png'
        thumbnail_path = settings.BASE_DIR / f"media/products/{self.thumbnail.name}"
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        description = ' '.join(self.description.split()[:30] + ['...']) if len(self.description.split()) > 30 else self.description
        return f"{self.name} | {description}"


class Receipt(models.Model):
    """User's Receipts"""
    slug = models.SlugField(_("Slug"), max_length=256, unique=True, blank=True)
    name = models.CharField(_("Name"), max_length=256, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    instructions = models.TextField(_("Instructions"))
    thumbnail = models.ImageField(upload_to='receipts')
    tags = models.ManyToManyField(Tag)
    youtube_link = models.CharField(_("YouTube link"), max_length=256, null=True, blank=True)
    products = models.ManyToManyField(Product)
    measures = models.ManyToManyField(Measure)
    source = models.CharField(_("Source link"), max_length=256, null=True, blank=True)
    cooking_difficulty = models.PositiveSmallIntegerField(_("Cooking difficulty"), null=True, blank=True)
    date_created = models.DateTimeField(_("Date created"), auto_now=True)

    def set_cooking_difficulty(self, diff):
        self.cooking_difficulty = diff
        super(Receipt, self).save()

    def make_products_with_measures(self):
        products = []
        for product, measure in zip(self.products.all(), self.measures.all()):
            products.append({
                'name': product.name,
                'slug': product.slug,
                'thumbnail': product.thumbnail.url,
                'amount': measure.amount,
                'unit': measure.unit
            })
        return products

    def get_tags(self):
        return "; ".join([tag.name for tag in self.tags.all()])
    get_tags.short_description = 'Tags'

    def get_absolute_url(self):
        return reverse("receipt_details", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.thumbnail.name = self.slug + '.png'
        thumbnail_path = settings.BASE_DIR / f"media/receipts/{self.thumbnail.name}"
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        super(Receipt, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = _('receipt')
        verbose_name_plural = _('receipts')

    def __str__(self):
        return f"{self.name} | {self.category.name} | {self.area.name}"
