from django.db import models

from shop.managers import OrderManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(null=True, blank=True, db_index=True)
    email_non_indexed = models.EmailField(null=True, blank=True)
    country = models.CharField(max_length=2)

    def save(self, *args, **kwargs):
        self.email_non_indexed = self.email
        return super().save(*args, **kwargs)


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    minumum_age_allowed = models.IntegerField(default=0)
    active = models.BooleanField(default=True)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name="products"
    )
    price = models.DecimalField(max_digits=16, decimal_places=2)
    active = models.BooleanField(default=True)


class Order(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders"
    )
    order_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    delivery_method = models.CharField(
        choices=(
            ("pickup", "Pickup"),
            ("delivery", "Delivery"),
            ("other", "other"),
        ),
        max_length=20,
    )
    total = models.DecimalField(max_digits=16, decimal_places=2)

    objects = OrderManager()

    def _calculate_total(self):
        self.total = self.items.all().aggregate(models.Sum("subtotal"))["subtotal__sum"]

    def save(self, *args, should_calculate_total=False, **kwargs):
        if should_calculate_total:
            self._calculate_total()
        return super().save(*args, **kwargs)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="items_sold"
    )
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price

        self.subtotal = self.unit_price * self.amount
        return super().save(*args, **kwargs)
