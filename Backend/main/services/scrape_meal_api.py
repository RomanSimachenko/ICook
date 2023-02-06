import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from main import models
from django.utils.text import slugify
from django.conf import settings

import requests
from pathlib import Path
from typing import List, Dict
import logging
import datetime
import urllib.request
import urllib.parse
import urllib.error
import string
import time


BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=BASE_DIR / f'logs/{datetime.datetime.now().strftime("%Y-%m-%d")}.log',
    filemode='w'
)

CATEGORIES_URL = "https://www.themealdb.com/api/json/v1/1/categories.php"
AREAS_URL = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
PRODUCTS_URL = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
RECEIPTS_URL = "https://www.themealdb.com/api/json/v1/1/search.php?f={char}"


def collect_categories() -> List[Dict[str, str]]:
    """Collects categories from the site API"""
    response = requests.get(url=CATEGORIES_URL).json()

    result_categories = []
    for category in response['categories']:
        result_categories.append({
            "category_name": category['strCategory'].strip(),
            "category_description": category['strCategoryDescription'].strip() if category['strCategoryDescription'] else '',
            "category_thumbnail": category['strCategoryThumb'].strip()
        })

    return result_categories


def load_categories() -> None:
    """Loads categories into the site DB"""
    categories = collect_categories()
    logging.info(f"Successfully scraped {len(categories)} categories, loading into the DB")

    for category in categories:
        response = requests.get(url=category['category_thumbnail']).content
        # initialize temporary file storage for images
        tmp_img = NamedTemporaryFile(delete=True)
        tmp_img.write(response)
        tmp_img.flush()

        if models.Category.objects.filter(name=category['category_name']).exists():
            db_category = models.Category.objects.get(name=category['category_name'])
            db_category.description = category['category_description']
            db_category.thumbnail = File(tmp_img)
            db_category.save()
        else:
            models.Category.objects.create(
                name=category['category_name'],
                description=category['category_description'],
                thumbnail=File(tmp_img)
            )
        time.sleep(0.1)

    logging.info("Loading categories successfully finished")


def collect_areas() -> List[Dict[str, str]]:
    """Collects areas from the site API"""
    areas = requests.get(url=AREAS_URL).json()

    result_areas = []
    for area in areas['meals']:
        result_areas.append({
            'area_name': area['strArea'].strip()
        })

    return result_areas


def load_areas() -> None:
    """Loads areas into the site DB"""
    areas = collect_areas()
    logging.info(f"Successfully scraped {len(areas)} areas, loading into the DB")

    for area in areas:
        area = 'Ukrainian' if area['area_name'].lower().strip() in ('russia', 'russian',) else area['area_name']
        if not models.Area.objects.filter(name=area).exists():
            models.Area.objects.create(name=area)

    logging.info("Loading areas successfully finished")


def collect_products() -> List[Dict[str, str]]:
    """Collects products from the site API"""
    products = requests.get(url=PRODUCTS_URL).json()

    result_products = []
    for product in products['meals']:
        result_products.append({
            'product_name': product['strIngredient'].strip(),
            'product_thumbnail': f"https://www.themealdb.com/images/ingredients/{product['strIngredient'] + '.png'}".strip(),
            'product_description': product['strDescription'].strip() if product['strDescription'] else '',
        })

    return result_products


def load_products() -> None:
    """Loads products into the site DB"""
    products = collect_products()
    logging.info(f"Successfully scraped {len(products)} products, loading into the DB")

    for product in products:
        image_name = slugify(product['product_name']) + '-small.png'
        image_path = settings.BASE_DIR / f"media/products/{image_name}"
        if Path.exists(image_path):
            os.remove(image_path)
        retrieve_url = urllib.parse.quote(product['product_thumbnail'].replace('.png', '-small.png'), safe=':/')
        try:
            urllib.request.urlretrieve(retrieve_url, image_path)
        except urllib.error.HTTPError:
            continue

        response = requests.get(url=product['product_thumbnail']).content
        # initialize temporary file storage for images
        tmp_img = NamedTemporaryFile(delete=True)
        tmp_img.write(response)
        tmp_img.flush()

        if models.Product.objects.filter(name=product['product_name']).exists():
            db_product = models.Product.objects.get(name=product['product_name'])
            db_product.thumbnail = File(tmp_img)
            db_product.description = product['product_description']
            db_product.save()
        else:
            models.Product.objects.create(
                name=product['product_name'],
                thumbnail=File(tmp_img),
                description=product['product_description']
            )
        time.sleep(0.1)

    logging.info("Loading products successfully finished")


def collect_receipts() -> List[Dict[str, str]]:
    """Collects receipts from the site API"""
    result_receipts = []

    for char in string.ascii_lowercase:
        response = requests.get(url=RECEIPTS_URL.format(char=char)).json()

        if not response['meals']:
            continue

        for receipt in response['meals']:
            result_receipts.append({
                'receipt_name': receipt['strMeal'].strip(),
                'receipt_category': receipt['strCategory'].strip(),
                'receipt_area': receipt['strArea'].strip(),
                'receipt_instructions': receipt['strInstructions'].strip(),
                'receipt_thumbnail': receipt['strMealThumb'].strip(),
                'receipt_tags': [tag.strip() for tag in receipt['strTags'].split(',')] if receipt['strTags'] else [],
                'receipt_youtube_link': receipt['strYoutube'].strip(),
                'receipt_products': [receipt[f'strIngredient{n}'].strip() for n in range(1, 21) if receipt[f'strIngredient{n}']],
                'receipt_measures': [receipt[f'strMeasure{n}'].strip() for n in range(1, 21) if receipt[f'strMeasure{n}']],
                'receipt_source': receipt['strSource'].strip() if receipt['strSource'] else ''
            })
        time.sleep(0.1)

    return result_receipts


def load_receipts() -> None:
    """Loads receipts into the site DB"""
    receipts = collect_receipts()
    logging.info(f"Successfully scraped {len(receipts)} receipts, loading into the DB")

    for receipt in receipts:
        image_name = slugify(receipt['receipt_name']) + '-small.png'
        image_path = settings.BASE_DIR / f"media/receipts/{image_name}"
        if Path.exists(image_path):
            os.remove(image_path)
        retrieve_url = urllib.parse.quote(receipt['receipt_thumbnail'] + '/preview', safe=':/')
        try:
            urllib.request.urlretrieve(retrieve_url, image_path)
        except urllib.error.HTTPError:
            continue

        response = requests.get(url=receipt['receipt_thumbnail']).content
        # initialize temporary file storage for images
        tmp_img = NamedTemporaryFile(delete=True)
        tmp_img.write(response)
        tmp_img.flush()

        area = 'Ukrainian' if receipt['receipt_area'].lower().strip() in ('russia', 'russian',) else receipt['receipt_area']
        if models.Receipt.objects.filter(name=receipt['receipt_name']).exists():
            new_receipt = models.Receipt.objects.get(name=receipt['receipt_name'])
            new_receipt.category = models.Category.objects.get(name=receipt['receipt_category'])
            new_receipt.area = models.Area.objects.get(name=area)
            new_receipt.instructions = receipt['receipt_instructions']
            new_receipt.thumbnail = File(tmp_img)
            new_receipt.youtube_link = receipt['receipt_youtube_link']
            new_receipt.source = receipt['receipt_source']
            new_receipt.save()
            new_receipt.tags.clear()
            new_receipt.products.clear()
            new_receipt.measures.clear()
        else:
            new_receipt = models.Receipt.objects.create(
                name=receipt['receipt_name'],
                category=models.Category.objects.get(name=receipt['receipt_category']),
                area=models.Area.objects.get(name=area),
                instructions=receipt['receipt_instructions'],
                thumbnail=File(tmp_img),
                youtube_link=receipt['receipt_youtube_link'],
                source=receipt['receipt_source']
            )
        # add all tags
        for tag_name in receipt['receipt_tags']:
            if not tag_name:
                continue
            if models.Tag.objects.filter(name=tag_name).exists():
                tag = models.Tag.objects.get(name=tag_name)
            else:
                tag = models.Tag.objects.create(name=tag_name)
            new_receipt.tags.add(tag)
        # add all products and their measures
        for product_name, measure_name in zip(receipt['receipt_products'], receipt['receipt_measures']):
            if not product_name or not measure_name:
                continue
            if models.Product.objects.filter(name__iexact=product_name).exists():
                product = models.Product.objects.get(name__iexact=product_name)
            else:
                continue
            try:
                amount, unit = measure_name.split()[0].strip(), ' '.join(measure_name.split()[1:]).strip()
                amount = amount.replace('.', ' ').replace('(', '').replace(')', '').replace('–', ' ').replace('/', ' ').replace('-', ' ')
                unit = unit.replace('.', ' ').replace('(', '').replace(')', '').replace('–', ' ').replace('/', ' ').replace('-', ' ')
            except TypeError:
                amount, unit = measure_name.split()[0].strip(), measure_name.split()[0].strip()
                amount = amount.replace('.', ' ').replace('(', '').replace(')', '').replace('–', ' ').replace('/', ' ').replace('-', ' ')
                unit = unit.replace('.', ' ').replace('(', '').replace(')', '').replace('–', ' ').replace('/', ' ').replace('-', ' ')
            try:
                amount = float(amount)
            except ValueError:
                amount, unit = 1, amount + ' ' + unit
            new_unit = ""
            for item in unit.strip().split():
                try:
                    float(item)
                except ValueError:
                    if item != 'x' and item != 'g' and item != '½':
                        new_unit += item + ' '
            new_unit = new_unit.lower().strip()
            if not new_unit:
                new_unit = 'items'
            if models.Measure.objects.filter(amount=int(amount), unit=new_unit).exists():
                measure = models.Measure.objects.get(amount=int(amount), unit=new_unit)
            else:
                measure = models.Measure.objects.create(amount=int(amount), unit=new_unit)
            new_receipt.products.add(product)
            new_receipt.measures.add(measure)
        time.sleep(0.1)

    logging.info("Loading receipts successfully finished")


def set_cooking_difficulty() -> None:
    max_products_count = max(receipt.products.count() for receipt in models.Receipt.objects.all())
    data_list = [0] * (max_products_count + 1)
    for receipt in models.Receipt.objects.all():
        data_list[receipt.products.count()] += 1
    average_products_count = data_list.index(max(data_list))
    for receipt in models.Receipt.objects.all():
        receipt.set_cooking_difficulty(receipt.products.count() * 3 // average_products_count)
    logging.info("Receipts cooking difficulty successfully set")


def main():
    logging.info("Starting collecting data(categories, areas, products, receipts)")
    start_time = time.perf_counter()
    load_categories()
    time.sleep(5)
    load_areas()
    time.sleep(5)
    load_products()
    time.sleep(5)
    load_receipts()
    set_cooking_difficulty()
    logging.info(f"All the data collected and loaded into DB for {int((time.perf_counter() - start_time) // 60)} minutes")

