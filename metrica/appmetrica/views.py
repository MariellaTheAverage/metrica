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
        {
            "product_list": product_list,
            "integerinput": False,
            "objectprompt": "Enter product name"
        }
    )

# view all metrics for a specific product
def view_product(request, product_id):
    if request.method == "GET":
        # db_id = request.GET['in-name-prod-id']
        db_id = product_id
        product = get_object_or_404(Product, pk=db_id)
        metrics = get_list_or_404(Metric, fk_product=db_id)
        return render(
            request,
            "appmetrica/product.html",
            {
                "product": product,
                "metric_list": metrics,
                "integerinput": False,
                "objectprompt": "Enter metric name"
            }
        )
    else:
        return HttpResponseRedirect(reverse('appmetrica:index'))

# view a graph for a specific metric in a product
def view_metric(request, product_id, metric_id):
    if request.method == "GET":
        data = []
        pid = request.GET['product-id']
        mid = request.GET['metric-id']
        product = get_object_or_404(Product, pk=pid)
        metric = get_object_or_404(Metric, pk=mid)
        rawdata = MetricValue.objects.filter(fk_metric=mid).all().values()
        # rawdata = get_list_or_404(MetricValue, fk_metric=mid)
        print(rawdata)
        
        for entry in rawdata:
            print(entry)
            data.append({"key": entry['int_timestamp'], "value": entry['int_value']})
            # data[entry.int_timestamp] = entry.int_value

        return render(
            request,
            "appmetrica/metric.html",
            {
                "product": product,
                "metric": metric,
                "data": data,
                "integerinput": True,
                "objectprompt": "Enter values"
            }
        )
        # return HttpResponse(f"Metric {mid} ({metric_name}) for product {pid} ({product_name})")
    else:
        return HttpResponseRedirect(reverse('appmetrica:index'))

# set a new metric value from systems (automated)
# captures a single timestamp-value pair and saves it into db
# may be possible to batch save 
@csrf_exempt
def submit_metric(request):
    if request.method == "POST":
        # get parameters of metric
        # product id is unnecessary
        # pid = request.POST['product']
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