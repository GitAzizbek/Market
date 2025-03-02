from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self, data=None, message=None, status=None, *args, **kwargs):
        response = {
            "data": data or [],
            "message": message or "",
            "status_code": status
        }

        super().__init__(data=response, status=status, *args, **kwargs)

class ErrorResponse(Response):
    def __init__(self, error=None, message=None, status=None, method=None, path=None, *args, **kwargs):
        response = {
            "error": error or "Bad request",
            "message": message or "",
            "status_code": status,
            "method": method,
            "path": path
        }

        super().__init__(data=response, status=status, *args, **kwargs)