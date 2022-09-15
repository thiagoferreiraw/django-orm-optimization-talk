from django.apps import apps
from django.db import models
from django.db.models import Prefetch


class OrderManager(models.Manager):
    def with_items(self):
        OrderItem = apps.get_model("shop", "OrderItem")

        prefetch_items = Prefetch(
            "items", queryset=OrderItem.objects.select_related("product__category")
        )
        return (
            self.get_queryset()
            .prefetch_related(prefetch_items)
            .select_related("customer")
        )
