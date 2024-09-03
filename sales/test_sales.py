from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from sales.models import Product, SalesRecord
from uuid6 import uuid7
from datetime import datetime, timedelta


class SalesRecordListViewTests(APITestCase):
    def setUp(self):
        """
        Set up test data for the SalesRecordListView tests.
        """
        self.product1 = Product.objects.create(
            id=uuid7(), name="Product 1", category="Category 1", price=10.00
        )
        self.product2 = Product.objects.create(
            id=uuid7(), name="Product 2", category="Category 2", price=20.00
        )

        self.sales_record1 = SalesRecord.objects.create(
            id=uuid7(),
            product=self.product1,
            quantity_sold=5,
            total_sales_amount=50.00,
            date_of_sale=datetime.now() - timedelta(days=1),
        )
        self.sales_record2 = SalesRecord.objects.create(
            id=uuid7(),
            product=self.product2,
            quantity_sold=3,
            total_sales_amount=60.00,
            date_of_sale=datetime.now(),
        )

    def test_get_sales_records(self):  # TBD: add test for empty string and null category filtering
        """
        Test retrieving the list of sales records.
        """
        url = reverse("sales-data")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_sales_records_by_category(self):
        """
        Test filtering sales records by product category.
        """
        url = reverse("sales-data")
        response = self.client.get(url, {"category": "Category 1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["product"]["name"], "Product 1")


class SalesRecordAggregateViewTests(APITestCase):
    def setUp(self):
        """
        Set up test data for the SalesRecordAggregateView tests.
        """
        self.product1 = Product.objects.create(
            id=uuid7(), name="Product 1", category="Category 1", price=10.00
        )
        self.product2 = Product.objects.create(
            id=uuid7(), name="Product 2", category="Category 2", price=20.00
        )

        self.sales_record1 = SalesRecord.objects.create(
            id=uuid7(),
            product=self.product1,
            quantity_sold=5,
            total_sales_amount=50.00,
            date_of_sale=datetime(year=2024, month=8, day=2),
        )
        self.sales_record2 = SalesRecord.objects.create(
            id=uuid7(),
            product=self.product2,
            quantity_sold=3,
            total_sales_amount=60.00,
            date_of_sale=datetime(year=2024, month=7, day=3),
        )
        self.sales_record3 = SalesRecord.objects.create(
            id=uuid7(),
            product=self.product1,
            quantity_sold=4,
            total_sales_amount=70.00,
            date_of_sale=datetime(year=2024, month=7, day=4),
        )

    def test_aggregate_sales_by_category(self):
        """
        Test aggregating sales records by product category.
        """
        url = reverse("sales-data-aggregate")
        response = self.client.get(url, {"aggregate_by": "category"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]["group"], "Category 1")
        self.assertAlmostEqual(response.data[0]["total_sales"], 120)
        self.assertAlmostEqual(response.data[0]["average_price"], Decimal(13.33))

        self.assertEqual(response.data[1]["group"], "Category 2")
        self.assertAlmostEqual(response.data[1]["total_sales"], 60)
        self.assertAlmostEqual(response.data[1]["average_price"], 20)

    def test_aggregate_sales_by_month(self):
        """
        Test aggregating sales records by month.
        """
        url = reverse("sales-data-aggregate")
        response = self.client.get(url, {"aggregate_by": "month"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]["group"], "2024-07")
        self.assertAlmostEqual(response.data[0]["total_sales"], 130)
        self.assertAlmostEqual(response.data[0]["average_price"], Decimal(18.57))

        self.assertEqual(response.data[1]["group"], "2024-08")
        self.assertAlmostEqual(response.data[1]["total_sales"], 50)
        self.assertAlmostEqual(response.data[1]["average_price"], 10)

    def test_invalid_aggregate_by_parameter(self):
        """
        Test response when an invalid aggregate_by parameter is provided.
        """
        url = reverse("sales-data-aggregate")
        response = self.client.get(url, {"aggregate_by": "invalid"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("aggregate_by", response.data)

    def test_missing_aggregate_by_parameter(self):
        """
        Test response when aggregate_by parameter is not provided.
        """
        url = reverse("sales-data-aggregate")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("aggregate_by", response.data)
