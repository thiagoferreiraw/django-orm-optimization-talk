from django.db.models import Avg, Count, Max, Min, Sum, Exists, OuterRef

from django.db.models import Prefetch

from shop.helpers import debug_queries, DebugTypes
from shop.models import Customer, Order, OrderItem, Product


@debug_queries()
def list_orders_bad(limit=5):
    orders = Order.objects.filter()[:limit]
    for order in orders:
        print(f"Order #{order.id} - {order.customer.name} - ${order.total}")


@debug_queries()
def list_orders_good(limit=5):
    orders = Order.objects.filter().select_related("customer")[:limit]
    for order in orders:
        print(f"Order #{order.id} - {order.customer.name} - ${order.total}")


@debug_queries()
def list_order_items_bad(order_id=1):
    order = Order.objects.get(id=order_id)
    print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
    for item in order.items.all():
        print("Product: ", item.product.name)
        print("Category: ", item.product.category.name)
        print("Subtotal: ", item.subtotal, "\n")


@debug_queries()
def list_order_items_good(order_id=1):
    order = Order.objects.select_related("customer").get(id=order_id)
    print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
    for item in order.items.all().select_related("product__category"):
        print("Product: ", item.product.name)
        print("Category: ", item.product.category.name)
        print("Subtotal: ", item.subtotal, "\n")


@debug_queries()
def list_multiple_orders_and_items_bad(limit=5):
    orders = Order.objects.filter()[:limit]
    for order in orders:
        print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
        for item in order.items.all():
            print("Product: ", item.product.name)
            print("Category: ", item.product.category.name)
            print("Subtotal: ", item.subtotal, "\n")


@debug_queries()
def list_multiple_orders_and_items_medium(limit=5):
    orders = Order.objects.select_related("customer").filter()[:limit]
    for order in orders:
        print(f"Printing Order #{order.id} - {order.customer.name}", "\n", "-" * 60)
        for item in order.items.all().select_related("product__category"):
            print("Product: ", item.product.name)
            print("Category: ", item.product.category.name)
            print("Subtotal: ", item.subtotal, "\n")


@debug_queries()
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


@debug_queries(DebugTypes.FULL)
def list_total_sold_for_email_good(email="bramirez@example.com"):
    # Uses the indexed email field
    total_sold_for_email = Order.objects.filter(
        customer__email="bramirez@example.com"
    ).aggregate(total_sold=Sum("total"))

    print(f"Total sold for {email}: ${total_sold_for_email['total_sold']}")

@debug_queries(DebugTypes.FULL)
def list_total_sold_for_email_bad(email="bramirez@example.com"):
    # Uses the non indexed email field
    total_sold_for_email = Order.objects.filter(
        customer__email_non_indexed="bramirez@example.com"
    ).aggregate(total_sold=Sum("total"))

    print(f"Total sold for {email}: ${total_sold_for_email['total_sold']}")


@debug_queries(DebugTypes.FULL)
def list_top_paying_customers(limit=5):
    top_customers = (
        Customer.objects.annotate(
            orders_placed=Count("orders"), total_value=Sum("orders__total")
        )
        .order_by("-total_value")
        .values_list("name", "orders_placed", "total_value")[:limit]
    )
    for name, orders_placed, total_value in top_customers:
        print("Customer: ", name)
        print("Orders placed: ", orders_placed)
        print("Total Value: ", total_value)


@debug_queries(DebugTypes.FULL)
def list_top_paying_customers(limit=5):
    top_customers = (
        Customer.objects.annotate(
            orders_placed=Count("orders"), total_value=Sum("orders__total")
        )
        .order_by("-total_value")
        .values_list("name", "orders_placed", "total_value")[:limit]
    )
    for name, orders_placed, total_value in top_customers:
        print("Customer: ", name)
        print("Orders placed: ", orders_placed)
        print("Total Value: ", total_value)


@debug_queries(DebugTypes.FULL)
def list_product_top_sales(has_sales=True, limit=5):
    produts_with_sales = (
        Product.objects.annotate(
            has_sales=Exists(OrderItem.objects.filter(product_id=OuterRef("id"))),
            total_sold=Sum("items_sold__subtotal"),
        )
        .filter(has_sales=has_sales)
        .order_by("-total_sold")
        .values_list("name", "total_sold")[:limit]
    )

    for name, total_sold in produts_with_sales:
        print("Product: ", name)
        print("Total Sold: ", total_sold, "\n")


def run_all():
    from shop import samples

    for name, sample in samples.__dict__.items():
        if not name.startswith("list_"):
            continue

        print(f"======== {name} ==========")
        sample()
