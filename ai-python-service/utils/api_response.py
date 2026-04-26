"""
Standardized API response wrapper for Python FastAPI
"""

from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime


class ApiResponse(BaseModel):
    """
    Standardized API response format
    """
    status: str
    data: Optional[Any] = None
    message: Optional[str] = None
    timestamp: str = datetime.now().isoformat()
    
    @classmethod
    def success(cls, data: Any = None, message: str = None) -> "ApiResponse":
        """Create a success response"""
        return cls(status="success", data=data, message=message)
    
    @classmethod
    def error(cls, message: str, data: Any = None) -> "ApiResponse":
        """Create an error response"""
        return cls(status="error", data=data, message=message)
    
    @classmethod
    def created(cls, data: Any = None, message: str = None) -> "ApiResponse":
        """Create a created response"""
        return cls(status="created", data=data, message=message)
    
    @classmethod
    def updated(cls, data: Any = None, message: str = None) -> "ApiResponse":
        """Create an updated response"""
        return cls(status="updated", data=data, message=message)
    
    @classmethod
    def deleted(cls, message: str = None) -> "ApiResponse":
        """Create a deleted response"""
        return cls(status="deleted", message=message)


class ErrorResponse(BaseModel):
    """
    Detailed error response
    """
    status: str = "error"
    error: str
    details: Optional[str] = None
    timestamp: str = datetime.now().isoformat()
    
    @classmethod
    def create(cls, error: str, details: str = None) -> "ErrorResponse":
        """Create an error response"""
        return cls(error=error, details=details)
