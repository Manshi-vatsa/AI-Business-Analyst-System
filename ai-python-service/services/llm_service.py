import logging
import os
import json
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class CriticalOpenAIError(Exception):
    """Exception for critical OpenAI errors that should trigger immediate fallback"""
    pass

class LLMService:
    """
    LLM Service for SQL generation using OpenAI with schema-aware prompting
    """
    
    def __init__(self):
        # Load and validate OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable is not set")
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        if not api_key.startswith('sk-'):
            logger.error("Invalid OpenAI API key format - should start with 'sk-'")
            raise ValueError("Invalid OpenAI API key format")
        
        try:
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise
        
        # Load model configuration with validation
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        if self.model not in ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo']:
            logger.warning(f"Unusual model name: {self.model}. Using gpt-4o-mini as fallback")
            self.model = 'gpt-4o-mini'
        
        self.max_retries = int(os.getenv('LLM_MAX_RETRIES', 3))
        self.temperature = float(os.getenv('LLM_TEMPERATURE', 0.1))
        
        logger.info(f"LLM Service initialized: model={self.model}, max_retries={self.max_retries}, temperature={self.temperature}")
        
        # Database schema for context
        self.db_schema = {
            "tables": [
                {
                    "name": "sales",
                    "columns": [
                        {"name": "id", "type": "INT", "description": "Primary key"},
                        {"name": "product", "type": "VARCHAR(255)", "description": "Product name"},
                        {"name": "quantity", "type": "INT", "description": "Quantity sold"},
                        {"name": "revenue", "type": "DECIMAL(10,2)", "description": "Revenue amount"},
                        {"name": "date", "type": "DATE", "description": "Sale date"},
                        {"name": "region", "type": "VARCHAR(100)", "description": "Sales region"}
                    ],
                    "sample_data": [
                        {"id": 1, "product": "Laptop", "quantity": 25, "revenue": 125000.00, "date": "2024-01-15", "region": "North"},
                        {"id": 2, "product": "Phone", "quantity": 35, "revenue": 70000.00, "date": "2024-01-16", "region": "South"}
                    ]
                },
                {
                    "name": "insights",
                    "columns": [
                        {"name": "id", "type": "INT", "description": "Primary key"},
                        {"name": "insight_type", "type": "VARCHAR(50)", "description": "Type of insight"},
                        {"name": "insight_data", "type": "JSON", "description": "Insight data"},
                        {"name": "created_at", "type": "TIMESTAMP", "description": "Creation timestamp"}
                    ]
                }
            ]
        }
        
        logger.info(f"LLMService initialized with model: {self.model}")
    
    def get_schema_context(self) -> str:
        """Generate schema context for the LLM"""
        schema_text = "DATABASE SCHEMA:\n\n"
        
        for table in self.db_schema["tables"]:
            schema_text += f"Table: {table['name']}\n"
            schema_text += "Columns:\n"
            for col in table["columns"]:
                schema_text += f"  - {col['name']} ({col['type']}) - {col['description']}\n"
            
            if "sample_data" in table:
                schema_text += "Sample Data:\n"
                for sample in table["sample_data"][:2]:  # Show only 2 samples
                    schema_text += f"  {json.dumps(sample, indent=2)}\n"
            schema_text += "\n"
        
        return schema_text
    
    def get_system_prompt(self) -> str:
        """Generate system prompt for SQL generation"""
        schema_context = self.get_schema_context()
        
        return f"""You are an expert SQL query generator for a business analytics database.

{schema_context}

RULES:
1. Generate ONLY valid MySQL SQL queries
2. Use proper table and column names from the schema
3. Include appropriate WHERE clauses for filtering
4. Use proper GROUP BY and ORDER BY when needed
5. Return ONLY the SQL query, no explanations
6. Handle date comparisons using proper MySQL date functions
7. Use appropriate aggregate functions (SUM, AVG, COUNT, MAX, MIN)
8. Limit results when appropriate (LIMIT 10 for general queries)

COMMON QUERY PATTERNS:
- Total sales: SELECT SUM(revenue) as total_sales FROM sales
- Average sales: SELECT AVG(revenue) as avg_sales FROM sales  
- Regional analysis: SELECT region, SUM(revenue) FROM sales GROUP BY region
- Product analysis: SELECT product, SUM(revenue) FROM sales GROUP BY product
- Time-based: Use DATE_FORMAT(date, '%Y-%m') for monthly grouping
- Top performers: ORDER BY revenue DESC LIMIT 1

Generate the most appropriate SQL query for the given natural language question."""

    def generate_sql_with_retry(self, question: str, steps: List[str]) -> str:
        """Generate SQL with immediate fallback on critical errors"""
        try:
            system_prompt = self.get_system_prompt()
            
            # Include steps in user prompt for better context
            user_prompt = f"""Natural Language Question: {question}

Analysis Steps: {', '.join(steps) if steps else 'General analysis'}

Generate most appropriate SQL query for this question."""
            
            logger.info(f"Generating SQL for question: {question}")
            logger.debug(f"Using model: {self.model}, temperature: {self.temperature}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=500,
                timeout=5.0  # 5 second timeout
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the SQL query
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            # Basic SQL validation
            if not sql_query.lower().startswith(('select', 'with')):
                raise ValueError(f"Generated query doesn't start with SELECT or WITH: {sql_query}")
            
            logger.info(f"Generated SQL: {sql_query}")
            return sql_query
            
        except Exception as e:
            # Categorize and log different types of OpenAI errors
            error_msg = str(e).lower()
            
            # Check for critical errors that should trigger immediate fallback
            if any(keyword in error_msg for keyword in [
                "rate limit", "429", "insufficient_quota", "quota", 
                "timeout", "connection", "model", "not found", "invalid_request"
            ]):
                logger.error(f"OpenAI critical error detected: {e}")
                logger.error("Switching to intelligent fallback SQL generation")
                raise CriticalOpenAIError(f"Critical OpenAI error: {e}")
            
            # For other errors, try one quick retry
            logger.warning(f"OpenAI non-critical error: {e}")
            logger.info("Attempting one quick retry...")
            try:
                # Quick retry with shorter timeout
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=500,
                    timeout=3.0  # 3 second timeout for retry
                )
                
                sql_query = response.choices[0].message.content.strip()
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
                
                if sql_query.lower().startswith(('select', 'with')):
                    logger.info(f"Retry successful: {sql_query}")
                    return sql_query
                    
            except Exception as retry_e:
                logger.error(f"Retry also failed: {retry_e}")
            
            # If retry fails, raise critical error to trigger fallback
            raise CriticalOpenAIError(f"OpenAI retry failed: {e}")
    
    def get_intelligent_fallback_sql(self, question: str) -> str:
        """Generate intelligent fallback SQL based on question patterns"""
        question_lower = question.lower()
        
        # Region-based queries
        if any(keyword in question_lower for keyword in ['region', 'regions', 'regional']):
            logger.info("Using fallback: Region-based query")
            return "SELECT region, SUM(revenue) as total_revenue, COUNT(*) as sales_count FROM sales GROUP BY region ORDER BY total_revenue DESC"
        
        # Monthly/period-based queries
        elif any(keyword in question_lower for keyword in ['month', 'monthly', 'period', 'time']):
            logger.info("Using fallback: Monthly query")
            return "SELECT DATE_FORMAT(date, '%Y-%m') as month, SUM(revenue) as total_revenue, COUNT(*) as sales_count FROM sales GROUP BY DATE_FORMAT(date, '%Y-%m') ORDER BY month DESC LIMIT 12"
        
        # Product/performance queries
        elif any(keyword in question_lower for keyword in ['product', 'products', 'top', 'best', 'performing']):
            logger.info("Using fallback: Product performance query")
            return "SELECT product, SUM(revenue) as total_revenue, COUNT(*) as sales_count FROM sales GROUP BY product ORDER BY total_revenue DESC LIMIT 10"
        
        # Sales/total queries
        elif any(keyword in question_lower for keyword in ['sales', 'total', 'revenue', 'sum']):
            logger.info("Using fallback: Total sales query")
            return "SELECT SUM(revenue) as total_sales, COUNT(*) as total_transactions, AVG(revenue) as avg_sale FROM sales"
        
        # Generic fallback
        else:
            logger.info("Using fallback: Generic query")
            return "SELECT * FROM sales ORDER BY date DESC LIMIT 100"

    def generate_sql(self, question: str, steps: List[str]) -> str:
        """Main method to generate SQL from natural language"""
        try:
            logger.info(f"=== LLM SQL GENERATION ===")
            logger.info(f"Question: {question}")
            logger.info(f"Steps: {steps}")
            
            # Generate SQL with immediate fallback
            sql_query = self.generate_sql_with_retry(question, steps)
            
            logger.info(f"SQL generated successfully")
            return sql_query
            
        except CriticalOpenAIError as e:
            logger.error(f"Critical OpenAI error: {e}")
            logger.error("Using intelligent fallback SQL generation")
            fallback_sql = self.get_intelligent_fallback_sql(question)
            logger.warning(f"Using intelligent fallback SQL: {fallback_sql}")
            return fallback_sql
            
        except Exception as e:
            logger.error(f"Failed to generate SQL: {e}")
            logger.error("Using intelligent fallback SQL generation")
            fallback_sql = self.get_intelligent_fallback_sql(question)
            logger.warning(f"Using intelligent fallback SQL: {fallback_sql}")
            return fallback_sql
    
    def validate_sql(self, sql_query: str) -> bool:
        """Basic SQL validation"""
        try:
            sql_lower = sql_query.lower().strip()
            
            # Check for basic SQL structure
            if not sql_lower.startswith(('select', 'with')):
                return False
            
            # Check for dangerous operations
            dangerous_keywords = ['drop', 'delete', 'truncate', 'alter', 'create', 'insert', 'update']
            for keyword in dangerous_keywords:
                if keyword in sql_lower:
                    logger.warning(f"Dangerous keyword detected: {keyword}")
                    return False
            
            # Check for required table presence
            if 'sales' not in sql_lower and 'insights' not in sql_lower:
                logger.warning("No valid table name found in query")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating SQL: {e}")
            return False
    
    def explain_sql(self, sql_query: str) -> str:
        """Generate explanation for SQL query (for debugging)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a SQL expert. Explain what this SQL query does in simple terms."},
                    {"role": "user", "content": f"Explain this SQL query: {sql_query}"}
                ],
                temperature=0.3,
                max_tokens=200,
                timeout=3.0  # 3 second timeout
            )
            
            explanation = response.choices[0].message.content.strip()
            logger.info(f"SQL explanation: {explanation}")
            return explanation
            
        except CriticalOpenAIError as e:
            logger.error(f"Critical OpenAI error in explain_sql: {e}")
            return f"SQL query explanation: This query retrieves data from the sales database"
        except Exception as e:
            logger.error(f"Error generating SQL explanation: {e}")
            return f"SQL query explanation: This query retrieves data from the sales database"

# Global LLM service instance
llm_service = LLMService()
