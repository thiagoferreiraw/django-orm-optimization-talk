from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    country = models.CharField(max_length=2)


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    minumum_age_allowed = models.IntegerField(default=0)
    active = models.BooleanField(default=True)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
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


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
