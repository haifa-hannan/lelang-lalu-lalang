from django.urls import path
from . import views

urlpatterns = [
    path("get-products/", views.GetProduct.as_view(), name="get-products"),
    path("add-products/", views.ProductViews.as_view(), name="add-products"),
    path("del-products/", views.DeleteProduct.as_view(), name="del-product"),
]