import time
from django.db import connection
from django.utils.deprecation import MiddlewareMixin


class SQLLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        total_time = time.time() - request.start_time
        print(f"Request took {total_time:.2f} seconds")
        queries = connection.queries
        for query in queries:
            print(f"SQL Query: {query['sql']} | Time: {query['time']}")
        return response
