from rest_framework import serializers
from sales.models import Product, SalesRecord


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Serializes the following fields:
        id (UUID): The unique identifier of the product.
        name (str): The name of the product.
        category (str): The category to which the product belongs.
    """

    class Meta:
        model = Product
        fields = ["id", "name", "category"]


class SalesRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the SalesRecord model, including nested product details.

    Serializes the following fields:
        id (UUID): The unique identifier of the sales record.
        product (ProductSerializer): The serialized product associated with this sales record.
        quantity_sold (int): The quantity of the product sold.
        total_sales_amount (Decimal): The total amount of sales for this record.
        date_of_sale (datetime): The date and time when the sale was made.
    """

    product = ProductSerializer()

    class Meta:
        model = SalesRecord
        fields = "__all__"


class AggregatedSalesRecordSerializer(serializers.Serializer):
    """
    Serializer for aggregated sales records.

    Serializes the following fields:
        group (datetime or str): The group by which the sales records are aggregated, formatted as a date (e.g., "YYYY-MM") or as a category.
        total_sales (Decimal): The total sales amount for the group.
        average_price (Decimal): The average price of the products sold in the group.
    """

    group = serializers.DateTimeField(format="%Y-%m")
    """
    ListModelMixin does not try to validate so this works for aggregate_by=category too.
    Can't guarantee that for future DRF versions so handling it explicitly might be better.
    """
    total_sales = serializers.DecimalField(max_digits=14, decimal_places=2)
    average_price = serializers.DecimalField(max_digits=9, decimal_places=2)
