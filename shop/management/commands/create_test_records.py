from random import choice, randint

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Count, Max, Min, Sum

from shop.factory import (
    CustomerFactory,
    OrderFactory,
    OrderItemFactory,
    ProductCategoryFactory,
    ProductFactory,
)
from shop.models import Customer, Order


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--total_customers", type=int, default=100, required=False)
        parser.add_argument("--total_categories", type=int, default=10, required=False)
        parser.add_argument("--total_products", type=int, default=100, required=False)
        parser.add_argument("--total_orders", type=int, default=100, required=False)
        parser.add_argument(
            "--max_items_per_order", type=int, default=6, required=False
        )

    def handle(self, *args, **options):
        customers, orders, categories, products = [], [], [], []

        for _ in range(options["total_customers"]):
            customers.append(CustomerFactory())

        for _ in range(options["total_categories"]):
            categories.append(ProductCategoryFactory())

        for _ in range(options["total_products"]):
            products.append(ProductFactory(category=choice(categories)))

        for _ in range(options["total_orders"]):
            orders.append(OrderFactory(customer=choice(customers)))

        for order in orders:
            for _ in range(randint(1, options["max_items_per_order"])):
                OrderItemFactory(product=choice(products), order=order)
            order.save(should_calculate_total=True)

        self.stdout.write(self.style.SUCCESS("Done!"))

        average_item_count_per_order = Order.objects.annotate(Count("items")).aggregate(
            items_count=Avg("items__count")
        )
        order_stats = Order.objects.aggregate(
            Avg("total"), Max("total"), Min("total"), Sum("total")
        )
        top_five_customers = (
            Customer.objects.annotate(orders_placed=Count("orders"))
            .order_by("-orders_placed")
            .values("name", "orders_placed")
        )[:5]

        self.stdout.write("*" * 100)
        self.stdout.write(
            f"average_item_count_per_order => {average_item_count_per_order}"
        )
        self.stdout.write(f"top_five_customers => {list(top_five_customers)}")
        self.stdout.write("Order totals")
        for key, value in order_stats.items():
            self.stdout.write(f"-- {key} => {value}")

        self.stdout.write("*" * 100)
