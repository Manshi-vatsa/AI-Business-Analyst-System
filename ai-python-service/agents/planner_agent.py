import logging
import re

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Planner Agent - converts user questions into execution steps
    """
    
    def __init__(self):
        pass
    
    def plan_query(self, question: str) -> list:
        """
        Convert user question into list of execution steps
        
        Input: user question
        Output: list of steps
        
        Examples:
        "Why did sales drop?" → ["get sales data", "compare months", "find drop"]
        "What are total sales?" → ["get sales data", "calculate total"]
        "Which region performed best?" → ["get sales data", "group by region", "find maximum"]
        """
        logger.info(f"Planning query: {question}")
        
        question_lower = question.lower()
        steps = []
        
        # Always start with getting data
        steps.append("get sales data")
        
        # Analyze question type to determine steps
        if any(word in question_lower for word in ["drop", "decrease", "decline", "fall"]):
            steps.extend(["compare time periods", "find drop percentage"])
            logger.info(f"Detected drop analysis question: {question}")
            
        elif any(word in question_lower for word in ["total", "sum", "overall"]):
            steps.append("calculate total")
            logger.info(f"Detected total calculation question: {question}")
            
        elif any(word in question_lower for word in ["average", "avg", "mean"]):
            steps.append("calculate average")
            logger.info(f"Detected average calculation question: {question}")
            
        elif any(word in question_lower for word in ["region", "area", "location"]):
            steps.extend(["group by region", "find best performer"])
            logger.info(f"Detected regional analysis question: {question}")
            
        elif any(word in question_lower for word in ["product", "item", "category"]):
            steps.extend(["group by product", "find top performer"])
            logger.info(f"Detected product analysis question: {question}")
            
        elif any(word in question_lower for word in ["compare", "vs", "versus", "difference"]):
            steps.append("compare metrics")
            logger.info(f"Detected comparison question: {question}")
            
        else:
            # Default analysis
            steps.append("analyze data")
            logger.info(f"Using default analysis for question: {question}")
        
        logger.info(f"Generated steps: {steps}")
        return steps
