import factory
import factory.fuzzy

from shop.models import Customer, Order, OrderItem, Product, ProductCategory


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker("name")
    birth_date = factory.Faker("date")
    country = factory.Iterator(["US", "BR", "AR"])


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory

    name = factory.Faker("name")
    minumum_age_allowed = factory.Iterator([21, 18, 18, 0, 0, 0])


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("name")
    description = factory.Faker("sentence")
    category = factory.SubFactory(ProductCategoryFactory)
    price = factory.fuzzy.FuzzyDecimal(0.5, 15)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    order_date = factory.Faker("date")
    is_paid = factory.Iterator([True, False])
    delivery_method = factory.Iterator(
        map(lambda x: x[0], Order.delivery_method.field.choices)
    )
    total = 0


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    amount = factory.fuzzy.FuzzyDecimal(0.1, 10)
