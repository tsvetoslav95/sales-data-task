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
- **Test Suite Improvements**: Enhance the existing test suite. The current tests (mostly chat gpt :) ) provide basic coverage, but additional, more comprehensive tests will improve reliability.

### Code Quality
- **Import Ordering**: Review and organize import statements according to best practices.

### Documentation
- **Enhanced API Schema**: Improve the API schema and documentation. Currently, the project uses `drf-spectacular`, but further refinements are needed, such as providing enums for the `aggregate_by` query parameter and removing unnecessary authentication inputs from the docs page.

### Authentication and Authorization
- **Authentication Mechanism**: Implement authentication (e.g., Token Auth, JWT, OAuth2) to secure the API.
- **Fine-Grained Permissions**: Once authentication is in place, implement fine-grained permission controls to manage access to resources.

### Pagination
- **Pagination Strategy**: Consider replacing the current pagination with cursor pagination, which may offer better performance and consistency, especially when the `end_date` filter is not used or is today. UUIDv7 primary keys could be leveraged for this purpose.
- **Evaluate Query Efficiency**: Determine whether `prefetch_related` or `select_related` is more appropriate for the `sales-data` endpoint. This decision will depend on the expected distribution of products and the frequency of category filtering.

### Database Optimization
- **UUIDv7 Support in PostgreSQL**: Explore methods to enable PostgreSQL to generate UUIDv7 identifiers natively.
- **UUID Usage**: Since using UUIDv7 as the primary key is still experimental, consider using incremental primary keys with an additional UUID field for lookups.

### Query Optimization
- **Aggregation Query Optimization**: Optimize the aggregation query to avoid redundant `SUM` and `CAST` operations. This will improve the efficiency and performance of the API. (see comment in code)
