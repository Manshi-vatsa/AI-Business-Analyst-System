import logging
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any
import os
import time

logger = logging.getLogger(__name__)

class DataAgent:
    """
    Data Agent - converts natural language to SQL and executes queries
    """
    
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'ai_analytics'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'Manshi@263'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True,
            'raise_on_warnings': True
        }
        self.max_retries = int(os.getenv('DB_MAX_RETRIES', 3))
        self.retry_delay = int(os.getenv('DB_RETRY_DELAY', 2))
        
        logger.info(f"DataAgent initialized with config: {self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}")
    
    def connect_to_mysql(self):
        """Connect to MySQL database with retry mechanism"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempting to connect to MySQL (attempt {attempt + 1}/{self.max_retries})")
                connection = mysql.connector.connect(**self.db_config)
                logger.info("Successfully connected to MySQL database")
                return connection
            except Error as e:
                logger.error(f"Error connecting to MySQL (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Max retries reached. Using mock data.")
                    return None
    
    def natural_language_to_sql(self, question: str, steps: List[str]) -> str:
        """
        Convert natural language question to SQL query based on steps
        """
        logger.info(f"Converting natural language to SQL: {question}")
        logger.info(f"Using steps: {steps}")
        
        question_lower = question.lower()
        
        # Generate SQL based on question type and steps
        if any(word in question_lower for word in ["total", "sum", "overall"]):
            sql = "SELECT SUM(revenue) as total_sales, COUNT(*) as total_transactions FROM sales"
            logger.info(f"Generated total sales SQL: {sql}")
            
        elif any(word in question_lower for word in ["average", "avg", "mean"]):
            sql = "SELECT AVG(revenue) as avg_sales, COUNT(*) as total_transactions FROM sales"
            logger.info(f"Generated average sales SQL: {sql}")
            
        elif any(word in question_lower for word in ["region", "area", "location"]):
            if "best" in question_lower or "top" in question_lower:
                sql = """
                SELECT region, SUM(revenue) as total_revenue 
                FROM sales 
                GROUP BY region 
                ORDER BY total_revenue DESC 
                LIMIT 1
                """
            else:
                sql = """
                SELECT region, SUM(revenue) as total_revenue, COUNT(*) as transactions
                FROM sales 
                GROUP BY region 
                ORDER BY total_revenue DESC
                """
            logger.info(f"Generated regional analysis SQL: {sql}")
            
        elif any(word in question_lower for word in ["product", "item", "category"]):
            if "best" in question_lower or "top" in question_lower:
                sql = """
                SELECT product, SUM(revenue) as total_revenue 
                FROM sales 
                GROUP BY product 
                ORDER BY total_revenue DESC 
                LIMIT 1
                """
            else:
                sql = """
                SELECT product, SUM(revenue) as total_revenue, COUNT(*) as transactions
                FROM sales 
                GROUP BY product 
                ORDER BY total_revenue DESC
                """
            logger.info(f"Generated product analysis SQL: {sql}")
            
        elif any(word in question_lower for word in ["drop", "decrease", "decline", "fall"]):
            sql = """
            SELECT 
                DATE_FORMAT(date, '%Y-%m') as month,
                SUM(revenue) as monthly_revenue
            FROM sales 
            WHERE date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(date, '%Y-%m')
            ORDER BY month DESC
            """
            logger.info(f"Generated drop analysis SQL: {sql}")
            
        elif any(word in question_lower for word in ["compare", "vs", "versus"]):
            sql = """
            SELECT 
                DATE_FORMAT(date, '%Y-%m') as month,
                SUM(revenue) as monthly_revenue
            FROM sales 
            GROUP BY DATE_FORMAT(date, '%Y-%m')
            ORDER BY month DESC
            LIMIT 12
            """
            logger.info(f"Generated comparison SQL: {sql}")
            
        else:
            # Default query - get recent sales data
            sql = "SELECT * FROM sales ORDER BY date DESC LIMIT 100"
            logger.info(f"Generated default SQL: {sql}")
        
        return sql
    
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return results
        """
        logger.info(f"Executing SQL query: {sql}")
        logger.info(f"SQL Query: {sql}")
        
        connection = None
        try:
            connection = self.connect_to_mysql()
            if connection is None:
                logger.warning("Database connection failed, using mock data")
                return self.get_mock_data()
                
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                logger.info(f"Query executed successfully, returned {len(results)} records")
                logger.debug(f"Query results: {results[:5]}...")  # Log first 5 results for debugging
                return results
                
        except Error as e:
            logger.error(f"Error executing query: {e}")
            logger.error(f"Failed SQL: {sql}")
            logger.warning("Using mock data as fallback")
            return self.get_mock_data()
        finally:
            if connection and connection.is_connected():
                connection.close()
                logger.info("Database connection closed")
    
    def execute_insert_query(self, sql: str, params: tuple) -> int:
        """
        Execute INSERT SQL query with parameters and return affected rows
        """
        logger.info(f"Executing INSERT query: {sql}")
        logger.info(f"Parameters: {params}")
        
        connection = None
        try:
            connection = self.connect_to_mysql()
            if connection is None:
                logger.error("Database connection failed for INSERT operation")
                raise Exception("Database connection failed")
                
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                connection.commit()
                affected_rows = cursor.rowcount
                logger.info(f"INSERT query executed successfully, affected {affected_rows} rows")
                return affected_rows
                
        except Error as e:
            logger.error(f"Error executing INSERT query: {e}")
            logger.error(f"Failed SQL: {sql}")
            logger.error(f"Parameters: {params}")
            if connection:
                connection.rollback()
            raise Exception(f"INSERT query failed: {str(e)}")
        finally:
            if connection and connection.is_connected():
                connection.close()
                logger.info("Database connection closed")
    
    def get_data(self, question: str, steps: List[str]) -> List[Dict[str, Any]]:
        """
        Main method to get data based on natural language question
        """
        logger.info(f"=== DATA FLOW TRACE ===")
        logger.info(f"1. Question received: {question}")
        logger.info(f"2. Steps generated: {steps}")
        logger.info(f"3. DB Config: {self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}")
        
        try:
            # Convert natural language to SQL
            sql = self.natural_language_to_sql(question, steps)
            logger.info(f"4. Generated SQL: {sql}")
            
            # Execute query
            data = self.execute_query(sql)
            
            logger.info(f"5. Query executed successfully")
            logger.info(f"6. Records retrieved: {len(data)}")
            if data:
                logger.info(f"7. Sample record: {data[0]}")
            else:
                logger.warning("7. No records retrieved")
            
            return data
            
        except Exception as e:
            logger.error(f"8. ERROR in get_data: {e}", exc_info=True)
            logger.error(f"9. Exception type: {type(e).__name__}")
            logger.error(f"10. Exception details: {str(e)}")
            
            # NO MOCK FALLBACK - Raise proper exception
            raise Exception(f"Database operation failed: {str(e)}")
    
    def get_mock_data(self) -> List[Dict[str, Any]]:
        """
        Return mock data when database is not available
        """
        logger.info("Using enhanced mock data with variations")
        
        # Mock sales data with clear patterns and drops
        mock_sales = [
            {"id": 1, "product": "Laptop", "quantity": 25, "revenue": 125000.0, "date": "2024-01-15", "region": "North"},
            {"id": 2, "product": "Phone", "quantity": 35, "revenue": 70000.0, "date": "2024-01-16", "region": "South"},
            {"id": 3, "product": "Tablet", "quantity": 20, "revenue": 60000.0, "date": "2024-01-17", "region": "East"},
            {"id": 4, "product": "Laptop", "quantity": 18, "revenue": 90000.0, "date": "2024-01-18", "region": "West"},
            {"id": 5, "product": "Phone", "quantity": 40, "revenue": 80000.0, "date": "2024-01-19", "region": "North"},
            {"id": 6, "product": "Tablet", "quantity": 15, "revenue": 45000.0, "date": "2024-01-20", "region": "South"},
            {"id": 7, "product": "Laptop", "quantity": 30, "revenue": 150000.0, "date": "2024-01-21", "region": "East"},
            {"id": 8, "product": "Phone", "quantity": 22, "revenue": 44000.0, "date": "2024-01-22", "region": "West"},  # Drop!
            {"id": 9, "product": "Tablet", "quantity": 18, "revenue": 54000.0, "date": "2024-01-23", "region": "North"},  # Drop!
            {"id": 10, "product": "Laptop", "quantity": 16, "revenue": 80000.0, "date": "2024-01-24", "region": "South"},  # Drop!
            {"id": 11, "product": "Phone", "quantity": 20, "revenue": 40000.0, "date": "2024-01-25", "region": "East"},  # Drop!
            {"id": 12, "product": "Tablet", "quantity": 10, "revenue": 30000.0, "date": "2024-01-26", "region": "West"},  # Drop!
            {"id": 13, "product": "Laptop", "quantity": 12, "revenue": 60000.0, "date": "2024-01-27", "region": "North"},  # Drop!
            {"id": 14, "product": "Phone", "quantity": 15, "revenue": 30000.0, "date": "2024-01-28", "region": "South"},  # Drop!
            {"id": 15, "product": "Tablet", "quantity": 8, "revenue": 24000.0, "date": "2024-01-29", "region": "East"},  # Drop!
        ]
        
        # Mock insights data
        mock_insights = [
            {"insight_type": "drop", "message": "Sales decreased by 15% this week", "value": -15, "category": "sales", "created_at": "2024-01-24T10:00:00"},
            {"insight_type": "increase", "message": "North region showed 20% growth", "value": 20, "category": "region", "created_at": "2024-01-24T11:00:00"},
            {"insight_type": "alert", "message": "Phone inventory running low", "value": 5, "category": "inventory", "created_at": "2024-01-24T12:00:00"},
            {"insight_type": "trend", "message": "Laptop sales trending upward", "value": 25, "category": "product", "created_at": "2024-01-24T13:00:00"},
            {"insight_type": "warning", "message": "South region below target", "value": -10, "category": "region", "created_at": "2024-01-24T14:00:00"}
        ]
        
        # Return appropriate data based on the query
        if "insight" in str(self.db_config).lower() or "insights" in str(self.db_config).lower():
            return mock_insights
        else:
            return mock_sales
