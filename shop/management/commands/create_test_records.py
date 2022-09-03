from random import choice, randint

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Count, Max, Min, Sum
from factory import LazyFunction

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
        parser.add_argument("--total_customers", type=int, default=1000, required=False)
        parser.add_argument("--total_categories", type=int, default=50, required=False)
        parser.add_argument("--total_products", type=int, default=1000, required=False)
        parser.add_argument("--total_orders", type=int, default=5000, required=False)
        parser.add_argument(
            "--max_items_per_order", type=int, default=6, required=False
        )

    def handle(self, *args, **options):
        customers, orders, categories, products = [], [], [], []

        self.stdout.write(f"Inserting test records with options = {options}")

        self.stdout.write(f"Inserting {options['total_customers']} Customers")
        customers = CustomerFactory.create_batch(options["total_customers"])

        self.stdout.write(f"Inserting {options['total_categories']} Categories")
        categories = ProductCategoryFactory.create_batch(options["total_categories"])

        self.stdout.write(f"Inserting {options['total_products']} Products")
        products = ProductFactory.create_batch(
            options["total_products"], category=LazyFunction(lambda: choice(categories))
        )

        self.stdout.write(f"Inserting {options['total_orders']} Orders")
        orders = OrderFactory.create_batch(
            options["total_orders"], customer=LazyFunction(lambda: choice(customers))
        )

        self.stdout.write(f"Creating order items...")
        for order in orders:
            OrderItemFactory.create_batch(
                randint(1, options["max_items_per_order"]),
                order=order,
                product=LazyFunction(lambda: choice(products)),
            )
            order.save(should_calculate_total=True)

        self.stdout.write(self.style.SUCCESS("Done!"))

        average_item_count_per_order = Order.objects.annotate(Count("items")).aggregate(
            items_count=Avg("items__count")
        )
        order_stats = Order.objects.aggregate(
            Avg("total"), Max("total"), Min("total"), Sum("total"), Count("id")
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
