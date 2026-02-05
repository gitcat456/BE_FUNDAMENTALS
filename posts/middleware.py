import time
import logging

logger = logging.getLogger("django.request")  
class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time setup

    def __call__(self, request):
        # Record start time
        start_time = time.time()

        # Log request info
        logger.info(f"Incoming request: {request.scheme} {request.method} {request.path}")

        # Call next middleware / view
        response = self.get_response(request)

        # Calculate elapsed time
        duration = time.time() - start_time

        # Log response info
        logger.info(
            f"Response: {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Time taken: {duration:.4f} sec"
        )

        return response
