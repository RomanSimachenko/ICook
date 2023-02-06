from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from . import serializers
from main import models


@api_view(['GET'])
def getRoutesView(request):
    routes = [
        'GET /api/v1',
        'GET /api/v1/categories',
        'GET /api/v1/areas',
        # 'GET /api/v1/measures',
        # 'GET /api/v1/tags',
        'GET /api/v1/products',
        'GET /api/v1/product-details/<slug:slug>',
        'GET /api/v1/receipts',
        'GET /api/v1/receipt-details/<slug:slug>',
    ]
    return Response(routes)


@api_view(['GET'])
def getCategoriesView(request):
    search = request.GET.get('search', '')
    categories = models.Category.objects.filter(
        Q(name__icontains=search) |
        Q(description__icontains=search)
    )
    serializer = serializers.CategorySerializer(categories, many=True)
    query_params = {key: value for key, value in request.GET.dict().items() if key and value}
    response_json = {
        "query_params": query_params,
        "total": len(categories),
        "categories": serializer.data
    }
    return Response(response_json)


@api_view(['GET'])
def getAreasView(request):
    search = request.GET.get('search', '')
    areas = models.Area.objects.filter(name__icontains=search)
    serializer = serializers.AreaSerializer(areas, many=True)
    query_params = {key: value for key, value in request.GET.dict().items() if key and value}
    response_json = {
        "query_params": query_params,
        "total": len(areas),
        "areas": serializer.data
    }
    return Response(response_json)


@api_view(['GET'])
def getProductsView(request):
    request_data = {}
    for item in request.path.rstrip('/').split('/')[-1].split(';'):
        tmp1 = item.split('=')
        if len(tmp1) == 2:
            if item.split('=')[1].strip() and item.split('=')[0].strip():
                request_data[item.split('=')[0].strip()] = item.split('=')[1].strip()

    search = request_data.get('search', '')
    try:
        page = int(request_data.get('page', 1))
    except ValueError:
        page = 1
    try:
        page_size = int(request_data.get('page_size', 12))
    except ValueError:
        page_size = 12

    page_size = 36 if page_size > 36 else page_size
    page_size = 12 if page_size < 12 else page_size
    products = models.Product.objects.filter(
        Q(name__icontains=search) |
        Q(description__icontains=search)
    )
    paginator = Paginator(products, per_page=page_size)
    page = 1 if page < 1 else page
    page = paginator.num_pages if page > paginator.num_pages else page

    serializer = serializers.ProductSerializer(paginator.get_page(page), many=True)
    query_params = dict(list({key: value for key, value in request.GET.dict().items() if key and value}.items()) +
                        list({key: value for key, value in request_data.items() if key and value}.items()))
    response_json = {
        "query_params": query_params,
        "page": page,
        "page_size": page_size,
        "on_page": len(serializer.data),
        "total": len(products),
        "products": serializer.data
    }
    return Response(response_json)


@api_view(['GET'])
def getProductDetailsView(request, slug):
    product = models.Product.objects.get(slug=slug)
    serializer = serializers.ProductDetailsSerializer(product, many=False)
    query_params = {key: value for key, value in request.GET.dict().items() if key and value}
    response_json = {
        "query_params": query_params,
        "product": serializer.data,
    }
    return Response(response_json)


@api_view(['GET'])
def getReceiptsView(request):
    request_data = {}
    for item in request.path.rstrip('/').split('/')[-1].split(';'):
        tmp1 = item.split('=')
        if len(tmp1) == 2:
            tmp2 = tmp1[1].split(',')
            if tmp1[0].strip().lower() in ('categories', 'areas', 'products', 'amounts',):
                some_list = [item2.lower().title() for item2 in tmp2 if item2.strip()]
                if some_list:
                    request_data[tmp1[0].strip()] = some_list
            else:
                if tmp1[1].strip() and tmp1[0].strip():
                    request_data[tmp1[0].strip()] = tmp1[1].strip()

    search = request_data.get('search', '')
    categories = request_data.get('categories', [category.name for category in models.Category.objects.all()])
    areas = request_data.get('areas', [area.name for area in models.Area.objects.all()])
    products = request_data.get('products', [])
    amounts = request_data.get('amounts', [])
    try:
        page = int(request_data.get('page', 1))
    except ValueError:
        page = 1
    try:
        page_size = int(request_data.get('page_size', 12))
    except ValueError:
        page_size = 12
    try:
        amounts = [int(amount) for amount in amounts]
    except ValueError:
        products = []
        amounts = []

    if products and amounts:
        receipts = []
        for receipt in models.Receipt.objects.all():
            matches_count, prods = 0, receipt.make_products_with_measures()
            for prod in prods:
                for p, amount in zip(products, amounts):
                    if prod['slug'] == p.lower() and prod['amount'] <= amount:
                        matches_count += 1
            if matches_count == len(prods):
                receipts.append(receipt.name)
        receipts = models.Receipt.objects.filter(name__in=receipts)
    else:
        receipts = models.Receipt.objects.all()

    page_size = 36 if page_size > 36 else page_size
    page_size = 12 if page_size < 12 else page_size
    receipts = receipts.filter(category__name__in=categories).filter(area__name__in=areas).filter(
        Q(name__icontains=search) |
        Q(instructions__icontains=search)
    )
    paginator = Paginator(receipts, per_page=page_size)
    page = 1 if page < 1 else page
    page = paginator.num_pages if page > paginator.num_pages else page

    serializer = serializers.ReceiptSerializer(paginator.get_page(page), many=True)
    query_params = dict(list({key: value for key, value in request.GET.dict().items() if key and value}.items()) +
                        list({key: value for key, value in request_data.items() if key and value}.items()))
    response_json = {
        "query_params": query_params,
        "page": page,
        "page_size": page_size,
        "on_page": len(serializer.data),
        "total": len(receipts),
        "receipts": serializer.data
    }
    return Response(response_json)


@api_view(['GET'])
def getReceiptDetailsView(request, slug):
    receipt = models.Receipt.objects.get(slug=slug)
    serializer = serializers.ReceiptDetailsSerializer(receipt, many=False)
    query_params = {key: value for key, value in request.GET.dict().items() if key and value}
    response_json = {
        "query_params": query_params,
        "receipt": serializer.data,
    }
    return Response(response_json)
