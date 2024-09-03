from django_filters import rest_framework as filters

from sales.models import SalesRecord


class EmptyStringFilterMixin:
    empty_value = "EMPTY_STR"  # Edge case: if a category is named EMPTY_STR we can not filter for it

    def filter(self, qs, value):
        if value != self.empty_value:
            return super().filter(qs, value)
        qs = self.get_method(qs)(**{"%s__%s" % (self.field_name, self.lookup_expr): ""})
        return qs.distinct() if self.distinct else qs


class IsNullStringFilterMixin:
    null_value = (
        "NOT_SET"  # Edge case: if a category is named NOT_SET we can not filter for it
    )

    def filter(self, qs, value):
        if value != self.null_value:
            return super().filter(qs, value)
        qs = self.get_method(qs)(**{"%s__%s" % (self.field_name, "isnull"): True})
        return qs.distinct() if self.distinct else qs


class IsNullEmptyFilter(
    EmptyStringFilterMixin, IsNullStringFilterMixin, filters.CharFilter
):
    pass


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
    category = IsNullEmptyFilter(field_name="product__category")

    class Meta:
        model = SalesRecord
        fields = ["start_date", "end_date", "category"]
