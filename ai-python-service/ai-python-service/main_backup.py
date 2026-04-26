from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from services.agent_pipeline import agent_pipeline
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
    """
    Get insights from MySQL insights table
    
    Returns structured data:
    [
      {
        "type": "drop",
        "message": "...",
        "value": -20
      }
    ]
    """
    logger.info("Fetching insights from MySQL insights table")
    
    try:
        # Fetch insights from database
        fetch_insights_query = """
            SELECT insight_type, message, value, category, created_at 
            FROM insights 
            ORDER BY created_at DESC 
            LIMIT 50
        """
        
        # Use data agent to execute query
        data_agent = DataAgent()
        insights_data = data_agent.execute_query(fetch_insights_query)
        
        if not insights_data:
            logger.warning("No insights found in database")
            return ApiResponse.success(
                data=[],
                message="No insights available"
            )
        
        # Format insights as required structure
        formatted_insights = []
        for insight in insights_data:
            formatted_insights.append({
                "type": insight.get('insight_type', 'unknown'),
                "message": insight.get('message', ''),
                "value": insight.get('value', 0),
                "category": insight.get('category', 'general'),
                "created_at": insight.get('created_at').isoformat() if insight.get('created_at') else None
            })
        
        logger.info(f"Retrieved {len(formatted_insights)} insights from database")
        return ApiResponse.success(
            data=formatted_insights,
            message="Insights retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error fetching insights from database: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create("Failed to fetch insights", str(e)).dict()
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
    Process natural language question using multi-agent pipeline
    
    - **question**: Natural language question about sales data
    
    Returns:
    {
        "answer": "...",
        "insights": ["..."]
    }
    """
    logger.info(f"Processing query through multi-agent pipeline: {request.question}")
    
    # Validate input
    if not request.question or not request.question.strip():
        raise ValidationException("Question cannot be empty")
    
    try:
        # Process the query using the multi-agent pipeline
        result = agent_pipeline.process_query(request.question)
        logger.debug(f"Multi-agent pipeline processed successfully for: {request.question}")
        
        # Create response data with required format
        response_data = {
            "answer": result["answer"],
            "insights": result["insights"]
        }
        
        # Add optional fields if available
        if "steps_executed" in result:
            response_data["steps_executed"] = result["steps_executed"]
        if "agent_logs" in result:
            response_data["agent_logs"] = result["agent_logs"]
        if "context" in result:
            response_data["context"] = result["context"]
        
        logger.info(f"Successfully processed query through pipeline: {request.question}")
        return ApiResponse.success(
            data=response_data,
            message="Query processed successfully through multi-agent pipeline"
        )
        
    except ValidationException as e:
        logger.warning(f"Validation error in query processing: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse.create(e.message, e.details).dict()
        )
    except Exception as e:
        logger.error(f"Unexpected error in multi-agent pipeline: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create("Failed to process query through pipeline", str(e)).dict()
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.get("/ai/dashboard", response_model=ApiResponse)
async def get_dashboard_data():
    """
    Get dashboard data with aggregated sales information
    
    Returns:
    {
        "monthlySales": [],
        "regionSales": [],
        "productSales": []
    }
    """
    logger.info("Generating dashboard data")
    
    try:
        # Use data agent to get all sales data
        data_agent = DataAgent()
        data = data_agent.get_data("get all sales data", ["get sales data"])
        
        if not data:
            logger.warning("No data available for dashboard")
            return ApiResponse.success(
                data={
                    "monthlySales": [],
                    "regionSales": [],
                    "productSales": []
                },
                message="No data available for dashboard"
            )
        
        # Use analysis agent to aggregate dashboard data
        analysis_agent = AnalysisAgent()
        dashboard_data = analysis_agent.aggregate_dashboard_data(data)
        
        logger.info(f"Dashboard data generated: {len(dashboard_data.get('monthlySales', []))} months, {len(dashboard_data.get('regionSales', []))} regions, {len(dashboard_data.get('productSales', []))} products")
        
        return ApiResponse.success(
            data=dashboard_data,
            message="Dashboard data retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error generating dashboard data: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.create("Failed to generate dashboard data", str(e)).dict()
        )

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
