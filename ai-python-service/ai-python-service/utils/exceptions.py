"""
Custom exceptions for Python FastAPI service
"""

from typing import Optional


class BaseBusinessException(Exception):
    """Base exception for business logic errors"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ValidationException(BaseBusinessException):
    """Exception for validation errors"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(message, details)


class ResourceNotFoundException(BaseBusinessException):
    """Exception for resource not found errors"""
    
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f" with identifier: {identifier}"
        super().__init__(message)


class ServiceUnavailableException(BaseBusinessException):
    """Exception for service unavailable errors"""
    
    def __init__(self, service: str, details: Optional[str] = None):
        message = f"{service} service is currently unavailable"
        super().__init__(message, details)


class DatabaseException(BaseBusinessException):
    """Exception for database-related errors"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(f"Database error: {message}", details)


class ReportGenerationException(BaseBusinessException):
    """Exception for report generation errors"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(f"Report generation error: {message}", details)


class QueryProcessingException(BaseBusinessException):
    """Exception for query processing errors"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(f"Query processing error: {message}", details)
