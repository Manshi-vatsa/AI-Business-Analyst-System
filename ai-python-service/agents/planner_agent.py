import logging

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Planner Agent - coordinates the query processing flow
    """
    
    def __init__(self):
        pass
    
    def plan_query(self, question: str) -> dict:
        """
        Plan the query processing approach
        """
        logger.info(f"Planning query: {question}")
        
        plan = {
            "question": question,
            "steps": ["analyze_question", "fetch_data", "generate_insights"],
            "status": "planned"
        }
        
        return plan
