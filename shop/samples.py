from sys import prefix

from django.db.models import Prefetch

from shop.helpers import debug_queries
from shop.models import Order, OrderItem


@debug_queries
def list_orders_bad(limit=5):
    orders = Order.objects.filter()[:limit]
    for order in orders:
        print(f"Order #{order.id} - {order.customer.name} - ${order.total}")


@debug_queries
def list_orders_good(limit=5):
    orders = Order.objects.filter().select_related("customer")[:limit]
    for order in orders:
        print(f"Order #{order.id} - {order.customer.name} - ${order.total}")


@debug_queries
def list_order_items_bad(order_id=1):
    order = Order.objects.get(id=order_id)
    print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
    for item in order.items.all():
        print("Product: ", item.product.name)
        print("Category: ", item.product.category.name)
        print("Subtotal: ", item.subtotal, "\n")


@debug_queries
def list_order_items_good(order_id=1):
    order = Order.objects.select_related("customer").get(id=order_id)
    print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
    for item in order.items.all().select_related("product__category"):
        print("Product: ", item.product.name)
        print("Category: ", item.product.category.name)
        print("Subtotal: ", item.subtotal, "\n")


@debug_queries
def list_multiple_orders_and_items_bad(limit=5):
    orders = Order.objects.filter()[:limit]
    for order in orders:
        print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
        for item in order.items.all():
            print("Product: ", item.product.name)
            print("Category: ", item.product.category.name)
            print("Subtotal: ", item.subtotal, "\n")


@debug_queries
def list_multiple_orders_and_items_medium(limit=5):
    orders = Order.objects.select_related("customer").filter()[:limit]
    for order in orders:
        print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
        for item in order.items.all().select_related("product__category"):
            print("Product: ", item.product.name)
            print("Category: ", item.product.category.name)
            print("Subtotal: ", item.subtotal, "\n")


@debug_queries
def list_multiple_orders_and_items_good(limit=5):
    prefetch_items = Prefetch(
        "items", queryset=OrderItem.objects.select_related("product__category")
    )
    orders = (
        Order.objects.select_related("customer")
        .prefetch_related(prefetch_items)
        .filter()[:limit]
    )
    for order in orders:
        print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
        for item in order.items.all():
            print("Product: ", item.product.name)
            print("Category: ", item.product.category.name)
            print("Subtotal: ", item.subtotal, "\n")
