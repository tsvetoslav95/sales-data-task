from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from sales.views import SalesRecordListView, SalesRecordAggregateView


urlpatterns = [
    path("sales-data/", SalesRecordListView.as_view(), name="sales-data"),
    path(
        "sales-data/aggregate",
        SalesRecordAggregateView.as_view(),
        name="sales-data-aggregate",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
