from django.db.models import Sum, F, FloatField
from django.db.models.functions import TruncMonth, Cast

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from sales.models import SalesRecord
from sales.serializers import SalesRecordSerializer, AggregatedSalesRecordSerializer
from sales.filters import SalesRecordFilter


class SalesRecordListView(ListAPIView):
    """
    API view to retrieve a list of sales records.

    Inherits from:
        ListAPIView: Provides a read-only endpoint to list sales records.

    Attributes:
        serializer_class (SalesRecordSerializer): The serializer class used to represent sales records.
        filterset_class (SalesRecordFilter): The filter class used for filtering sales records.
        pagination_class (LimitOffsetPagination): The pagination class to handle pagination of the sales records list.
        queryset (QuerySet): The base queryset to retrieve sales records.
    """

    serializer_class = SalesRecordSerializer
    filterset_class = SalesRecordFilter
    pagination_class = LimitOffsetPagination
    queryset = SalesRecord.objects.prefetch_related(
        "product"
    )
    """
    select_related is usually chosen for forward FK and since we have filter by product__category it might be more efficient in some cases.
    prefetch_related can be more efficient if SalesRecords vastly outnumber their related unique Products which is usually the case.
    Despite having one more db request, the data transfer is less.
    """


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name="aggregate_by", type=str),
        ]
    )
)
class SalesRecordAggregateView(ListAPIView):

    serializer_class = AggregatedSalesRecordSerializer
    filterset_class = SalesRecordFilter
    queryset = SalesRecord.objects.all()
    AGGREGATE_TYPES_MAPPER = {
        "category": F("product__category"),
        "month": TruncMonth("date_of_sale"),
    }

    def get_queryset(self):
        if not (
            aggregate_by := self.AGGREGATE_TYPES_MAPPER.get(
                self.request.query_params.get("aggregate_by")
            )
        ):
            raise ValidationError(
                {
                    "aggregate_by": f"param is required. Options are {list(self.AGGREGATE_TYPES_MAPPER.keys())}"
                }
            )

        queryset = (
            super()
            .get_queryset()
            .values(group=aggregate_by)
            .annotate(
                total_sales=Sum("total_sales_amount"),
                average_price=Cast(F("total_sales"), FloatField())
                / Sum("quantity_sold"),
            )
            .order_by("group")
        )
        """"
        This should be the most classic "Django" way to get the aggregates.
        SQL generated by ORM does not reuse SUM total_sales_amount
        so in SQL we have SUM total_sales_amount twice which is suboptimal.
        Also there is one redundant cast to Numeric before casting to Real (using Expression Wrapper results in the same SQL).
        Possible ways to optimize the query could be subquery so SUM total_sales_amount is reused or CTE.
        """
        return queryset
