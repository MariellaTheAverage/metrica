from django.urls import path

from . import views

app_name = 'appmetrica'
urlpatterns = [
    # ex: /appmetrica/
    path("", views.index, name="index"),
    # ex: /appmetrica/submit
    path("submit/", views.submit_metric, name="submit"),
    # ex: /appmetrica/product/
    path("<str:product_name>/", views.view_product, name="product"),
    # ex: /appmetrica/product/metric/
    path("<str:product_name>/<str:metric_name>/", views.view_metric, name="metric")
]