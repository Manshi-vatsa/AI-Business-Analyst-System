import pymysql
from typing import Optional, List, Dict, Any
import logging
from sql_generator import sql_generator

logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Enhanced database service with SQL execution capabilities
    """
    
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Manshi@263',
            'database': 'ai_analytics',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.connection: Optional[pymysql.Connection] = None
    
    def connect(self) -> pymysql.Connection:
        """Establish database connection"""
        try:
            if not self.connection or not self.connection.open:
                self.connection = pymysql.connect(**self.config)
                logger.info("Database connection established successfully")
            return self.connection
        except pymysql.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise Exception(f"Failed to connect to database: {e}")
    
    def disconnect(self):
        """Close database connection"""
        try:
            if self.connection and self.connection.open:
                self.connection.close()
                logger.info("Database connection closed")
        except pymysql.Error as e:
            logger.error(f"Error closing database connection: {e}")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        try:
            # Validate query before execution
            if not sql_generator.validate_query(query):
                raise Exception("Invalid or unsafe SQL query")
            
            logger.info(f"Executing query: {query}")
            connection = self.connect()
            
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                logger.info(f"Query executed successfully, returned {len(results)} rows")
                return results
                
        except pymysql.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise Exception(f"Failed to execute query: {e}")
        finally:
            self.disconnect()
    
    def execute_natural_language_query(self, question: str) -> Dict[str, Any]:
        """
        Execute a natural language query by converting it to SQL first
        """
        try:
            # Convert natural language to SQL
            sql_query = sql_generator.convert_to_sql(question)
            
            # Execute the generated SQL
            results = self.execute_query(sql_query)
            
            return {
                "question": question,
                "sql_query": sql_query,
                "results": results,
                "row_count": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error executing natural language query: {e}")
            raise Exception(f"Failed to process query: {e}")
    
    def get_table_schema(self, table_name: str = None) -> Dict[str, Any]:
        """Get schema information for tables"""
        try:
            connection = self.connect()
            
            if table_name:
                # Get specific table schema
                query = f"DESCRIBE {table_name}"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    columns = cursor.fetchall()
                    return {
                        "table": table_name,
                        "columns": columns
                    }
            else:
                # Get all tables
                query = "SHOW TABLES"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    tables = cursor.fetchall()
                    return {
                        "tables": [list(table.values())[0] for table in tables]
                    }
                    
        except pymysql.Error as e:
            logger.error(f"Error getting table schema: {e}")
            raise Exception(f"Failed to get schema: {e}")
        finally:
            self.disconnect()
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
        finally:
            self.disconnect()
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get comprehensive database information"""
        try:
            # Test connection
            is_connected = self.test_connection()
            
            # Get table info
            schema_info = self.get_table_schema()
            
            # Get sample data from sales table
            sample_data = None
            try:
                sample_data = self.execute_query("SELECT * FROM sales LIMIT 5")
            except Exception as e:
                logger.warning(f"Could not get sample data: {e}")
            
            return {
                "connected": is_connected,
                "database": "ai_analytics",
                "tables": schema_info.get("tables", []),
                "sample_sales_data": sample_data
            }
            
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {
                "connected": False,
                "error": str(e)
            }

# Global database service instance
db_service = DatabaseService()
