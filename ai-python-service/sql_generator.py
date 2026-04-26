import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SQLGenerator:
    """
    Natural language to SQL converter using rule-based approach
    """
    
    def __init__(self):
        """
        Initialize SQL generator
        """
        logger.info("SQL Generator initialized with rule-based approach")
    
    def convert_to_sql(self, question: str) -> str:
        """
        Convert natural language question to SQL query using rule-based approach
        """
        try:
            logger.info(f"Converting to SQL: {question}")
            sql_query = self._rule_based_sql_generation(question)
            logger.info(f"Generated SQL: {sql_query}")
            return sql_query
                
        except Exception as e:
            logger.error(f"Error in SQL generation: {e}")
            # Default fallback query
            return "SELECT * FROM sales LIMIT 50;"
    
    def _clean_sql_query(self, query: str) -> str:
        """Clean and format the generated SQL query"""
        # Remove any markdown formatting
        query = query.replace("```sql", "").replace("```", "").strip()
        
        # Ensure the query ends with semicolon
        if not query.endswith(';'):
            query += ';'
            
        return query
    
    def _rule_based_sql_generation(self, question: str) -> str:
        """
        Rule-based SQL generation as fallback
        """
        question_lower = question.lower().strip()
        
        # Handle "total sales" queries
        if "total sales" in question_lower or "sum of sales" in question_lower:
            return "SELECT SUM(revenue) as total_sales FROM sales;"
        
        # Handle "top products" queries
        elif "top products" in question_lower or "best products" in question_lower:
            return "SELECT product, SUM(revenue) as total_revenue FROM sales GROUP BY product ORDER BY total_revenue DESC LIMIT 10;"
        
        # Handle "sales by region" queries
        elif "sales by region" in question_lower or "regional sales" in question_lower:
            return "SELECT region, SUM(revenue) as total_revenue FROM sales GROUP BY region ORDER BY total_revenue DESC;"
        
        # Handle "average sales" queries
        elif "average sales" in question_lower or "mean sales" in question_lower:
            return "SELECT AVG(revenue) as average_sales FROM sales;"
        
        # Handle "count" queries
        elif "count" in question_lower and "sales" in question_lower:
            return "SELECT COUNT(*) as total_sales_count FROM sales;"
        
        # Handle "highest" or "maximum" queries
        elif "highest" in question_lower or "maximum" in question_lower or "max" in question_lower:
            return "SELECT MAX(revenue) as max_revenue FROM sales;"
        
        # Handle "lowest" or "minimum" queries
        elif "lowest" in question_lower or "minimum" in question_lower or "min" in question_lower:
            return "SELECT MIN(revenue) as min_revenue FROM sales;"
        
        # Handle "recent" queries
        elif "recent" in question_lower or "latest" in question_lower:
            return "SELECT * FROM sales ORDER BY date DESC LIMIT 10;"
        
        # Default query - show all sales with limit
        else:
            return "SELECT * FROM sales LIMIT 50;"
    
    def get_table_info(self) -> str:
        """Get information about available tables"""
        try:
            if self.db:
                return self.db.get_table_info()
            else:
                return "Database connection not available"
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            return "Error retrieving table information"
    
    def validate_query(self, query: str) -> bool:
        """Basic validation of SQL query"""
        try:
            # Basic checks
            if not query.strip():
                return False
            
            query_lower = query.lower()
            
            # Only allow SELECT statements for safety
            if not query_lower.strip().startswith('select'):
                logger.warning(f"Non-SELECT query blocked: {query}")
                return False
            
            # Block dangerous keywords
            dangerous_keywords = ['drop', 'delete', 'truncate', 'update', 'insert', 'alter']
            for keyword in dangerous_keywords:
                if keyword in query_lower:
                    logger.warning(f"Dangerous keyword '{keyword}' found in query: {query}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating query: {e}")
            return False

# Global SQL generator instance
sql_generator = SQLGenerator()
