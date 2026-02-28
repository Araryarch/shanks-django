"""Base DTO for standardized API responses"""


class BaseDTO:
    """Standard API response structure"""
    
    @staticmethod
    def success(data=None, message="Success", status=200, pagination=None):
        """
        Create a successful response
        
        Args:
            data: Response data (default: None)
            message: Success message (default: "Success")
            status: HTTP status code (default: 200)
            pagination: Pagination info dict (default: None)
        
        Returns:
            dict: Standardized response
        """
        response = {
            "status": status,
            "message": message,
            "data": data if data is not None else []
        }
        
        if pagination:
            response["pagination"] = pagination
        else:
            response["pagination"] = {
                "page": 1,
                "limit": 10,
                "total": 0,
                "pages": 0
            }
        
        return response
    
    @staticmethod
    def error(message="Error", status=400, data=None):
        """
        Create an error response
        
        Args:
            message: Error message (default: "Error")
            status: HTTP status code (default: 400)
            data: Additional error data (default: None)
        
        Returns:
            dict: Standardized error response
        """
        response = {
            "status": status,
            "message": message,
            "data": data if data is not None else []
        }
        
        return response
