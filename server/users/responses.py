from rest_framework.response import Response

class SuccessResponse(Response):
    def __init__(self, data=None, status=None, message=None, *args, **kwargs):
        response = {
            "data": data or [],
            "message": message,
            "status_code": status
        } 
        super().__init__(data=response, status=status, *args, **kwargs)
        

class ErrorResponse(Response):
    def __init__(self, error=None, message=None, status=None, path=None, method=None, *args, **kwargs):
        response = {
            "error": error,
            "message": message,
            "status_code": status,
            "path": path,
            "method": method
        }
        
        super().__init__(data=response, status=status, *args, **kwargs)