from django.urls import path
from . import views

urlpatterns = [
    path("get-products/", views.GetProduct.as_view(), name="get-products"),
    path("add-products/", views.ProductViews.as_view(), name="add-products"),
    path("del-products/", views.DeleteProduct.as_view(), name="del-product"),
    # path("upd-products/", views.UpdateProduct.as_view(), name="upd-product"),
    path("upd2-products/", views.UpdateProduct2.as_view(), name="upd2-product"),
    path("up-status/", views.UpdateStatus.as_view(), name="up-status"),
    path("transactions/", views.TransactionViews.as_view(), name="transactions"),
    path("get-transactions/", views.GetTransaction.as_view(), name="get-transactions"),
]