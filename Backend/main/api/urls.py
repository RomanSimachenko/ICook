from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.getRoutesView, name="routes"),

    path('categories/', views.getCategoriesView, name="categories"),

    path('areas/', views.getAreasView, name="areas"),

    # path('measures/', views.getMeasures, name="measures"),

    # path('tags/', views.getTags, name="tags"),

    re_path(r'products/', views.getProductsView, name="products"),
    path('product-details/<slug:slug>/', views.getProductDetailsView, name="product_details"),

    re_path('receipts/', views.getReceiptsView, name="receipts"),
    path('receipt-details/<slug:slug>/', views.getReceiptDetailsView, name="receipt_details"),
]