from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from agents.query_agent import query_agent
from services.insight_service import insight_service
from report_service import report_service
from utils.api_response import ApiResponse, ErrorResponse
from utils.exceptions import (
    ValidationException, 
    ResourceNotFoundException, 
    ServiceUnavailableException,
    DatabaseException,
    ReportGenerationException,
    QueryProcessingException
)
from utils.logging_config import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Business Analyst Service",
    description="A FastAPI service for natural language to SQL queries",
    version="1.0.0"
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    question: str
    
    class Config:
        schema_extra = {
            "example": {
                "question": "total sales"
            }
        }

class QueryResponse(BaseModel):
    answer: str
    insights: List[str]
    sql_query: Optional[str] = ""
    results: Optional[List[Dict[str, Any]]] = []
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "Total sales is 145000",
                "insights": ["North region contributes highest revenue"],
                "sql_query": "SELECT SUM(revenue) as total_sales FROM sales;",
                "results": [{"total_sales": 145000}]
            }
        }

class ReportRequest(BaseModel):
    report_type: str  # "pdf" or "ppt"
    
    class Config:
        schema_extra = {
            "example": {
                "report_type": "pdf"
            }
        }

class ReportResponse(BaseModel):
    status: str
    report_type: str
    filename: Optional[str] = None
    content_type: Optional[str] = None
    data: Optional[str] = None  # Base64 encoded report data
    insights: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "report_type": "pdf",
                "filename": "business_analytics_report_20240419_172500.pdf",
                "content_type": "application/pdf",
                "insights": {"total_revenue": 15500.0},
                "message": "PDF report generated successfully"
            }
        }

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

@app.get("/", response_model=ApiResponse)
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return ApiResponse.success(
        data={
            "message": "AI Business Analyst Service",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "query": "/ai/query",
                "insights": "/ai/insights",
                "report": "/ai/report"
            }
        },
        message="Service information retrieved successfully"
    )

@app.get("/health", response_model=ApiResponse)
async def health_check():
    """Health check endpoint"""
    logger.info("Health check accessed")
    return ApiResponse.success(
        data={
            "status": "healthy",
            "service": "AI Business Analyst Service"
        },
        message="Service is healthy"
    )

@app.get("/ai/insights", response_model=ApiResponse)
async def get_insights():
    """Get automatic insights from sales data"""
    logger.info("Generating insights from sales data")
    
    try:
        # Generate insights from sales data using pandas
        insights = insight_service.analyze_sales_data()
        logger.debug(f"Generated insights: {len(insights)} items")
        
        # Store insights in database
        insight_service.store_insights(insights)
        logger.info("Insights stored in database successfully")
        
        return ApiResponse.success(
            data=insights,
            message="Insights generated and stored successfully"
        )
        
    except DatabaseException as e:
        logger.error(f"Database error generating insights: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ErrorResponse.create("Database service unavailable", e.details).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error generating insights: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create("Failed to generate insights", str(e)).dict()
        )

@app.post("/ai/report", response_model=ApiResponse)
async def generate_report(request: ReportRequest):
    """
    Generate PDF or PowerPoint report with summary and insights
    
    - **report_type**: "pdf" or "ppt"
    """
    logger.info(f"Generating {request.report_type} report")
    
    # Validate input
    if request.report_type not in ["pdf", "ppt"]:
        raise ValidationException("report_type must be 'pdf' or 'ppt'")
    
    try:
        # Generate report using report service
        result = report_service.generate_report(request.report_type)
        
        if result["status"] == "error":
            raise ReportGenerationException(
                result.get("error", "Unknown error occurred"),
                result.get("details")
            )
        
        logger.info(f"{request.report_type.upper()} report generated successfully")
        return ApiResponse.success(
            data={
                "report_type": result["report_type"],
                "filename": result.get("filename"),
                "content_type": result.get("content_type"),
                "data": result.get("data"),
                "insights": result.get("insights")
            },
            message=result.get("message", f"{request.report_type.upper()} report generated successfully")
        )
        
    except ValidationException as e:
        logger.warning(f"Validation error in report generation: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse.create(e.message, e.details).dict()
        )
    except ReportGenerationException as e:
        logger.error(f"Report generation error: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ErrorResponse.create(e.message, e.details).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error generating report: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create("Failed to generate report", str(e)).dict()
        )

@app.post("/ai/query", response_model=ApiResponse)
async def query_ai(request: QueryRequest):
    """
    Process natural language question and return AI-generated insights
    
    - **question**: Natural language question about sales data
    """
    logger.info(f"Processing query: {request.question}")
    
    # Validate input
    if not request.question or not request.question.strip():
        raise ValidationException("Question cannot be empty")
    
    try:
        # Process the query using the agent
        result = query_agent.process_query(request.question)
        logger.debug(f"Query processed successfully for: {request.question}")
        
        # Create response data
        response_data = {
            "answer": result["answer"],
            "insights": result["insights"],
            "sql_query": result.get("sql_query", ""),
            "results": result.get("results", [])
        }
        
        logger.info(f"Successfully processed query: {request.question}")
        return ApiResponse.success(
            data=response_data,
            message="Query processed successfully"
        )
        
    except ValidationException as e:
        logger.warning(f"Validation error in query processing: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse.create(e.message, e.details).dict()
        )
    except QueryProcessingException as e:
        logger.error(f"Query processing error: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ErrorResponse.create(e.message, e.details).dict()
        )
    except DatabaseException as e:
        logger.error(f"Database error in query processing: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=ErrorResponse.create("Database service unavailable", e.details).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create("Failed to process query", str(e)).dict()
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Custom general exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal server error",
        "details": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
