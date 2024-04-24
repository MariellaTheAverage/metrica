from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Product, Metric, MetricValue
from django.urls import reverse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# view all products
def index(request):
    product_list = get_list_or_404(Product)
    # print(product_list[0].pk)
    if not product_list:
        raise Http404("List is empty")
    return render(
        request, 
        "appmetrica/index.html", 
        {"product_list": product_list}
    )

# view all metrics for a specific product
def view_product(request, product_name):
    if request.POST:
        db_id = request.POST['in-name-prod-id']
        product = get_object_or_404(Product, pk=db_id)
        metrics = get_list_or_404(Metric, fk_product=db_id)
        return render(
            request,
            "appmetrica/product.html",
            {
                "product": product,
                "metric_list": metrics
            }
        )
        # return HttpResponse(product)
    else:
        return HttpResponseRedirect(reverse('appmetrica:index'))

# view a graph for a specific metric in a product
def view_metric(request, product_name, metric_name):
    if request.method == "POST":
        pid = request.POST['product-id']
        mid = request.POST['metric-id']
        product = get_object_or_404(Product, pk=pid)
        metric = get_object_or_404(Metric, pk=mid)
        data = get_list_or_404(MetricValue, fk_metric=mid)
        return render(
            request,
            "appmetrica/metric.html",
            {
                "product": product,
                "metric": metric,
                "data": data
            }
        )
        # return HttpResponse(f"Metric {mid} ({metric_name}) for product {pid} ({product_name})")
    else:
        return HttpResponseRedirect(reverse('appmetrica:index'))

# set a new metric value from systems (automated)
@csrf_exempt
def submit_metric(request):
    if request.method == "POST":
        # get parameters of metric
        # insert into db
        pid = request.POST['product']
        mid = request.POST['metric']
        tstamp = request.POST['timestamp']
        value = request.POST['value']

        metric = get_object_or_404(Metric, pk=mid)

        insert = MetricValue(fk_metric=metric, int_timestamp=tstamp, int_value=value)
        try:
            insert.save()
        except Exception as e:
            print(e)
        else:
            return HttpResponse("OK")
    else:
        return render(request, "appmetrica/submit.html")