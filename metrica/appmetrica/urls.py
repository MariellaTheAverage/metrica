from django.urls import path

from . import views

app_name = 'appmetrica'
urlpatterns = [
    # ex: /appmetrica/
    path("", views.index, name="index"),
    # ex: /appmetrica/submit
    path("submit/", views.submit_metric, name="submit"),
    # ex: /appmetrica/product_id/
    path("<int:product_id>/", views.view_product, name="product"),
    # ex: /appmetrica/product_id/metric_id/
    path("<int:product_id>/<int:metric_id>/", views.view_metric, name="metric")
]