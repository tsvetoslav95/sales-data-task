from django_filters import rest_framework as filters

from sales.models import SalesRecord


class SalesRecordFilter(filters.FilterSet):
    """
    A filter set for filtering sales records based on specific criteria.

    Filters:
        start_date (DateTimeFilter): Filters sales records to include only those with a sale date greater than or equal to this date.
        end_date (DateTimeFilter): Filters sales records to include only those with a sale date less than or equal to this date.
        category (CharFilter): Filters sales records by the category of the related product.

    Meta:
        model (SalesRecord): The model on which the filters are applied.
        fields (list): A list of fields that can be used to filter the sales records.
    """

    start_date = filters.DateTimeFilter(
        field_name="date_of_sale", lookup_expr="date__gte"
    )
    end_date = filters.DateTimeFilter(
        field_name="date_of_sale", lookup_expr="date__lte"
    )
    category = filters.CharFilter(field_name="product__category")

    class Meta:
        model = SalesRecord
        fields = ["start_date", "end_date", "category"]
