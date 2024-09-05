from django.urls import path

from . import views

app_name = 'appmetrica'
urlpatterns = [
    # ex: /appmetrica/
    path("", views.index, name="index"),
    path("addmetric/", views.add_metric, name="add_metric"),
    path("addproduct/", views.add_product, name="add_product"),
    # ex: /appmetrica/submit
    path("submit/", views.submit_metric, name="submit"),
    path("delproduct/", views.delete_product, name="delproduct"),
    path("delmetric", views.delete_metric, name="delmetric"),
    path("delvalue/", views.delete_metricvalue, name="delvalue"),
    # ex: /appmetrica/product_id/
    path("<int:product_id>/", views.view_product, name="product"),
    # ex: /appmetrica/product_id/metric_id/
    path("<int:product_id>/<int:metric_id>/", views.view_metric, name="metric")
]