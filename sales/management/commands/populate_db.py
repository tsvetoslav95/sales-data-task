from django.core.management.base import BaseCommand
from sales.factories import ProductFactory, SalesRecordFactory


class Command(BaseCommand):

    def handle(self, *args, **options):
        ProductFactory.create_batch(200)
        SalesRecordFactory.create_batch(10000)
