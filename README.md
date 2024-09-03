# Sales Records API

This project provides an API for managing and aggregating sales records. It is built using Django and Django REST Framework, with features like filtering, pagination, and aggregation. The API documentation is provided via Swagger.

## Setup Instructions

To set up the project in a fresh Python environment with Python 3.10, follow these steps:

1. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Populate the database with initial data**:
   ```bash
   python manage.py populate_db
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Run the tests**:
   ```bash
   python manage.py test
   ```

6. **Try it out**:

[Swagger UI](http://localhost:8000/api/schema/swagger-ui/)

   ```bash
   curl http://localhost:8000/api/sales-data/ # (swagger does not like loading this one with no filters)
   curl http://localhost:8000/api/sales-data/aggregate?aggregate_by=month
   curl http://localhost:8000/api/sales-data/aggregate?aggregate_by=category
   ```
## API Documentation

Once the server is running, you can access the API documentation via Swagger:

[Swagger UI](http://localhost:8000/api/schema/swagger-ui/)

## Future Enhancements

If more time is available, the following improvements and features are planned:

### Database
- **PostgreSQL Integration**: Replace SQLite with PostgreSQL for production-level database management.

### Development Workflow
- **Separate Development Dependencies**: Create a `requirements-dev.txt` file to manage development-specific dependencies.

### Docker Integration
To streamline the setup and deployment process, Docker integration is planned. This will include:

- **Dockerfile**: A Dockerfile will be created to containerize the Django application. This ensures that the application runs consistently in any environment.

- **docker-compose.yml**: A Docker Compose configuration file will be added to manage multi-container setups, such as the application itself, the database, and other services (e.g., caching, messaging).
### Testing
- **Test Suite Improvements**: Enhance the existing test suite. The current tests (mostly chat gpt :) ) provide basic coverage, but additional, more comprehensive tests will improve reliability. Currently they do not cover null and empty string category filtering.

### Code Quality
- **Import Ordering**: Review and organize import statements according to best practices.

### Documentation
- **Enhanced API Schema**: Improve the API schema and documentation. Currently, the project uses `drf-spectacular`, but further refinements are needed, such as providing enums for the `aggregate_by` query parameter and removing unnecessary authentication inputs from the docs page. 

### Authentication and Authorization
- **Authentication Mechanism**: Implement authentication (e.g., Token Auth, JWT, OAuth2) to secure the API.
- **Fine-Grained Permissions**: Once authentication is in place, implement fine-grained permission controls to manage access to resources.

### Pagination
- **Pagination Strategy**: Consider replacing the current pagination with cursor pagination, which may offer better performance and consistency, especially when the `end_date` filter is not used or is today. UUIDv7 primary keys could be leveraged for this purpose.

### Edge cases
- **Empty string or null category filter**: As we are have hardcoded "magic" values EMPTY_STR and NOT_SET in category filter we can not filter by categories named this way
- **Empty string or null category aggregation**: Should be taken into account that categories can be both empty string and null which is a bad practice. These are 2 different categories and appear separately in aggregated data.

### Non-Edge cases:
- **DB handles zero division well**: Having returns (negative quantity) in sales record can result in zero divison in aggregation query. DB handles it well and we get null for average_price.
- **Integer divison in DB**: In aggregation query for average_price if all summed amounts are integers the result is rounded to integer. That's why we need the explicit cast to Float.

### Database Optimization
- **UUIDv7 Support in PostgreSQL**: Explore methods to enable PostgreSQL to generate UUIDv7 identifiers natively.
- **UUID Usage**: Since using UUIDv7 as the primary key is still experimental, consider using incremental primary keys with an additional UUID field for lookups.

### Query Optimization
- **Aggregation Query Optimization**: Optimize the aggregation query to avoid redundant `SUM` and `CAST` operations.  [see comment in code](https://github.com/tsvetoslav95/sales-data-task/blob/ef8a7248d017408093194c5d9e1251c3964749fa/sales/views.py#L77)
- **Evaluate Query Efficiency**: Determine whether `prefetch_related` or `select_related` is more appropriate for the `sales-data` endpoint. This decision will depend on the expected distribution of products accross sales records and the frequency of category filtering.

