from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Product, Metric, MetricValue
from django.urls import reverse

# view all products
def index(request):
    product_list = get_list_or_404(Product)
    # print(product_list[0].pk)
    if not product_list:
        raise Http404("List is empty")
    return render(request, "appmetrica/index.html", {"product_list": product_list})

# view all metrics for a specific product
def view_product(request, product_name):
    if request.POST:
        db_id = request.POST['in-name-prod-id']
        product = get_object_or_404(Product, pk=db_id)
        return HttpResponse(product)
    else:
        return HttpResponseRedirect(reverse('appmetrica:index'))

# view a graph for a specific metric in a product
def view_metric(request, product_id, metric_id):
    return HttpResponse("Here be graph")
