from datetime import datetime

from django.db import models

from uuid6 import uuid7


class UUIDv7Model(models.Model):
    """
    An abstract base model that provides a UUIDv7 primary key.

    We might call this premature optimization but using UUIDv4 for primary key comes with performance penalty on inserts
    as due to lack of subsequent ordering it is hard to index. UUIDv7 is new and creates an external dependency but it
    is supposed to do the job fine. I generally avoid using uuid as pk if not required.

    Attributes:
        id (UUID): The universally unique identifier (UUID) for this object, generated using UUIDv7.
    """

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)

    class Meta:
        abstract = True


class Product(UUIDv7Model):
    """
    Represents a product available for sale.

    Attributes:
        name (str): The name of the product.
        category (str): The category to which the product belongs. Indexed for faster lookup.
        price (Decimal): The price of the product, with up to 8 digits in total and 2 decimal places.
    """

    name = models.CharField(max_length=128)
    category = models.CharField(max_length=64, null=True, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.category} / {self.name}"


class SalesRecord(UUIDv7Model):
    """
    Represents a record of a sale transaction.

    Attributes:
        product (ForeignKey): A foreign key linking the sales record to a specific product.
        quantity_sold (int): The quantity of the product sold. Consider using PositiveIntegerField if returns are not allowed.
        total_sales_amount (Decimal): The total amount of sales for this transaction, with up to 9 digits in total and 2 decimal places.
        date_of_sale (datetime): The date and time when the sale was made. Indexed for faster querying by date.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    total_sales_amount = models.DecimalField(max_digits=9, decimal_places=2)
    date_of_sale = models.DateTimeField(default=datetime.now, db_index=True)

    def __str__(self):
        return f"{self.quantity_sold} * {self.product}"
