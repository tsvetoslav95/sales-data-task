from datetime import datetime, timezone

import factory
from faker import Faker
import faker_commerce
from sales.models import Product, SalesRecord


faker = Faker()
faker.add_provider(faker_commerce.Provider)


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(faker.ecommerce_name)
    category = factory.LazyFunction(faker.ecommerce_category)  # TBD: add null and empty str
    price = factory.Faker(
        "pydecimal", positive=True, min_value=1, max_value=1000, right_digits=2
    )

    class Meta:
        model = Product


class SalesRecordFactory(factory.django.DjangoModelFactory):
    product = factory.iterator(Product.objects.all)
    quantity_sold = factory.Faker("pyint", min_value=1, max_value=999)
    total_sales_amount = factory.LazyAttribute(
        lambda sr: sr.product.price * sr.quantity_sold
    )
    date_of_sale = factory.LazyFunction(
        lambda: faker.date_time_between(start_date=datetime(2022, 1, 1), end_date="now")
    )

    class Meta:
        model = SalesRecord
