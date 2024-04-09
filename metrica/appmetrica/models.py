from django.db import models
import time

class Product(models.Model):
    def __str__(self) -> str:
        return self.str_name
    
    str_name = models.CharField(max_length=500)

class Metric(models.Model):
    def __str__(self) -> str:
        return f"{self.str_name} in {self.fk_product.str_name}"
    
    str_name = models.CharField(max_length=500)
    fk_product = models.ForeignKey(Product, on_delete=models.RESTRICT)

class MetricValue(models.Model):
    def __str__(self) -> str:
        return f"{self.int_timestamp}: {self.int_value}"
    
    int_timestamp = models.IntegerField(default=int(time.time()))
    int_value = models.IntegerField(default=0)
    fk_metric = models.ForeignKey(Metric, on_delete=models.RESTRICT)
