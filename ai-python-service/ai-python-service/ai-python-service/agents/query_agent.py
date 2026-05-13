import logging
from typing import Dict, Any
from services import query_service

logger = logging.getLogger(__name__)

class QueryAgent:
    """
    AI Agent for handling business intelligence queries
    """
    
    def __init__(self):
        self.name = "Query Agent"
        self.description = "Handles natural language queries for sales analytics"
    
    def process_query(self, question: str) -> Dict[str, Any]:
        """
        Process a natural language query through the service layer
        """
        logger.info(f"{self.name} processing query: {question}")
        
        try:
            result = query_service.process_question(question)
            logger.info(f"Query processed successfully: {result['answer']}")
            return result
            
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return {
                "answer": f"Agent error: {str(e)}",
                "insights": []
            }

# Global agent instance
query_agent = QueryAgent()
