class PostViewLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        print("Request just entered middleware")
        
        #above runs before the view
        response = self.get_response(request)
        #below runs after the view 
        
        if request.path.startswith("/api/"):
            print(f"Post accessed: {request.path}")
        return response 