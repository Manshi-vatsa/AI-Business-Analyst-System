from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
from agents.planner_agent import PlannerAgent
from agents.data_agent import DataAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent
from db.connection import DatabaseConnection
from report_service_working import ReportService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Analytics Service",
    description="AI-powered business analytics service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
planner_agent = PlannerAgent()
data_agent = DataAgent()
analysis_agent = AnalysisAgent()
report_agent = ReportAgent()
report_service = ReportService()

# Pydantic models
class QueryRequest(BaseModel):
    question: str

class ReportRequest(BaseModel):
    report_type: str  # "pdf" or "ppt"

class QueryResponse(BaseModel):
    answer: str
    insights: List[str]

class InsightsResponse(BaseModel):
    insights: List[Dict[str, Any]]

class HealthResponse(BaseModel):
    status: str

class ReportResponse(BaseModel):
    status: str
    report_type: str
    filename: Optional[str] = None
    content_type: Optional[str] = None
    data: Optional[str] = None  # Base64 encoded report data
    message: Optional[str] = None

# Database connection for insights endpoint
db_connection = DatabaseConnection()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Analytics Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/ai/query",
            "insights": "/ai/insights"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/ai/query", response_model=QueryResponse)
async def query_ai(request: QueryRequest):
    """
    Process natural language question using agent flow
    """
    try:
        logger.info(f"Processing query: {request.question}")
        
        # Agent flow: PlannerAgent → DataAgent → AnalysisAgent → ReportAgent
        plan = planner_agent.plan_query(request.question)
        
        # Fetch data
        sales_data = data_agent.fetch_sales_data()
        
        # Analyze data
        analysis_result = analysis_agent.analyze_data(sales_data, request.question)
        
        # Generate final report
        final_result = report_agent.generate_report(analysis_result)
        
        return QueryResponse(
            answer=final_result["answer"],
            insights=final_result["insights"]
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/ai/insights", response_model=InsightsResponse)
async def get_insights():
    """
    Fetch stored insights from MySQL table "insights"
    """
    try:
        logger.info("Fetching stored insights")
        
        connection = db_connection.connect()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM insights ORDER BY created_at DESC")
            results = cursor.fetchall()
            
            insights = []
            for result in results:
                insights.append({
                    "id": result.get("id"),
                    "insight_type": result.get("insight_type"),
                    "insight_data": result.get("insight_data"),
                    "created_at": result.get("created_at")
                })
            
            logger.info(f"Fetched {len(insights)} stored insights")
            return {"insights": insights}
            
    except Exception as e:
        logger.error(f"Error fetching insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch insights: {str(e)}"
        )

@app.post("/ai/report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate PDF or PowerPoint report with summary and insights
    
    - **report_type**: "pdf" or "ppt"
    """
    try:
        logger.info(f"Generating {request.report_type} report")
        
        # Generate summary and insights
        sales_data = data_agent.fetch_sales_data()
        analysis_result = analysis_agent.analyze_data(sales_data, "Generate summary and insights")
        
        summary = analysis_result["answer"]
        insights = analysis_result["insights"]
        
        # Generate report based on type
        if request.report_type.lower() == "pdf":
            report_data = report_service.generate_pdf_report(summary, insights)
            content_type = "application/pdf"
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        elif request.report_type.lower() == "ppt":
            report_data = report_service.generate_ppt_report(summary, insights)
            content_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid report type. Supported types: pdf, ppt"
            )
        
        # Encode report data for transmission
        encoded_data = base64.b64encode(report_data).decode('utf-8')
        
        logger.info(f"{request.report_type.upper()} report generated successfully")
        return ReportResponse(
            status="success",
            report_type=request.report_type,
            filename=filename,
            content_type=content_type,
            data=encoded_data,
            message=f"{request.report_type.upper()} report generated successfully"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate {request.report_type} report: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
