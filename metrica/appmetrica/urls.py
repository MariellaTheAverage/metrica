from django.urls import path

from . import views

app_name = 'appmetrica'
urlpatterns = [
    # ex: /appmetrica/
    path("", views.index, name="index"),
    # ex: /appmetrica/product/
    path("<str:product_name>/", views.view_product, name="product"),
    # ex: /appmetrica/product/metric/
    path("<str:product_name>/<str:metric_name>/", views.view_metric, name="metric"),
    # ex: /polls/5/vote/
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]