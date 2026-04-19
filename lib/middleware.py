import time
import logging
from django.shortcuts import redirect
from django.urls import reverse


logger = logging.getLogger("django.request")  
class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time setup

    def __call__(self, request):
        # Record start time
        start_time = time.time()   

        # Log request info
        logger.info(f"Incoming request: \n Scheme: {request.scheme} \n Method: {request.method} \n Path: {request.path}")
        
        if request.path == '/':
            if request.user.is_authenticated:
                # Role is on the User model — "borrower" is not a role; member/customer borrow books.
                if request.user.role in ('member', 'customer'):
                    return redirect('/api/posts/')
                if request.user.role in ('admin', 'librarian'):
                    return redirect('/api/loan-list/')
                return redirect('/api/posts/')
            else:
                return redirect('/api/auth/jwt-login/')
                    
                 
                
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
