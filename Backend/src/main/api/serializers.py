from rest_framework import serializers
from django.db.models import fields
from src.main import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = '__all__'


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Measure
        fields = ('amount', 'unit',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('name', 'slug', 'thumbnail',)


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    category = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = models.Receipt
        fields = ('name', 'slug', 'category', 'area', 'thumbnail', 'cooking_difficulty', 'date_created',)


class ReceiptDetailsSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    category = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    tags = TagSerializer(many=True, read_only=True)
    products = serializers.ListField(source='make_products_with_measures')

    class Meta:
        model = models.Receipt
        exclude = ('measures', 'id',)
