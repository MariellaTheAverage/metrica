from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from .models import Product, Metric, MetricValue
from django.urls import reverse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from django.forms.models import model_to_dict

# view all products
def index(request):
    rawproducts = Product.objects.all()
    product_list = [p for p in rawproducts]
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
        rawmetrics = Metric.objects.filter(fk_product=db_id)
        metrics = [m for m in rawmetrics]
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
        # pid = request.GET['product-id']
        # mid = request.GET['metric-id']
        product = get_object_or_404(Product, pk=product_id)
        metric = get_object_or_404(Metric, pk=metric_id)
        rawdata = MetricValue.objects.filter(fk_metric=metric_id).all().values()
        # rawdata = get_list_or_404(MetricValue, fk_metric=mid)
        # print(rawdata)
        
        for entry in rawdata:
            # print(entry)
            data.append({
                "key": entry['int_timestamp'],
                "value": entry['int_value'],
                "id": entry["id"]
                })
            # data[entry.int_timestamp] = entry.int_value

        data.sort(key=lambda d: d['key'])

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
        rawdata = json.loads(request.body.decode('utf-8'))
        # get parameters of metric
        # product id is unnecessary
        mid = rawdata['metric']
        tstamp = rawdata['timestamp']
        value = rawdata['value']
        res = api_save_metric_value(mid, tstamp, value)
        if res:
            rspns = model_to_dict(res)
            rspns["res"] = "OK"
            return JsonResponse(rspns)
        else:
            return JsonResponse({ res: "NO" })
    else:
        # change
        return HttpResponseRedirect(reverse("appmetrica:index"))
    
def api_save_metric_value(mid, ts, val):
    metric = get_object_or_404(Metric, pk=mid)
    if not metric:
        return False
    insert = MetricValue(fk_metric=metric, int_timestamp=ts, int_value=val)
    try:
        insert.save()
    except Exception as e:
        print(e)
        return None
    else:
        return insert

@csrf_exempt    
def add_metric(request):
    if request.method == "POST":
        rawdata = json.loads(request.body.decode('utf-8'))
        metric_name = rawdata['metr-name']
        product_id = rawdata['prod-id']
        new_metric = Metric(str_name=metric_name, fk_product_id=product_id)
        rspns = {
            "status": "OK",
            "newmetric": model_to_dict(new_metric)
        }
        try:
            new_metric.save()
            rspns['newmetric'] = model_to_dict(new_metric)
        except Exception as e:
            print(e)
            rspns['status'] = e
            return JsonResponse(rspns)
        else:
            return JsonResponse(rspns)
    return HttpResponseBadRequest("POST")

@csrf_exempt
def add_product(request):
    if request.method == "POST":
        rawdata = json.loads(request.body.decode('utf-8'))
        product_name = rawdata['prod-name']
        new_product = Product(str_name=product_name)
        rspns = {
            "status": "OK",
            "newproduct": model_to_dict(new_product)
        }
        try:
            new_product.save()
            rspns['newproduct'] = model_to_dict(new_product)
        except Exception as e:
            print(e)
            rspns['status'] = e
            return JsonResponse(rspns)
        else:
            return JsonResponse(rspns)
    return HttpResponseBadRequest("POST")

@csrf_exempt
def delete_metricvalue(request):
    if request.method == "POST":
        rawdata = json.loads(request.body.decode('utf-8'))
        mvid = rawdata['mvid']
        target_value = MetricValue.objects.get(id=mvid)
        # print(model_to_dict(target_value))
        target_value.delete()
        return HttpResponse("OK")
    return HttpResponseBadRequest("POST")

# todo: add cascade deletion
@csrf_exempt
def delete_metric(request):
    if request.method == "POST":
        rawdata = json.loads(request.body.decode('utf-8'))
        mid = rawdata['mid']
        target_value = Metric.objects.get(id=mid)
        # print(model_to_dict(target_value))
        target_value.delete()
        return HttpResponse("OK")
    return HttpResponseBadRequest("POST")

# todo: add cascade deletion
@csrf_exempt
def delete_product(request):
    if request.method == "POST":
        rawdata = json.loads(request.body.decode('utf-8'))
        pid = rawdata['pid']
        target_value = Product.objects.get(id=pid)
        # print(model_to_dict(target_value))
        target_value.delete()
        return HttpResponse("OK")
    return HttpResponseBadRequest("POST")
