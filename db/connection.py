import pymysql
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
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
    
    def execute_query(self, query: str) -> list:
        """Execute SQL query and return results"""
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info(f"Query executed successfully, returned {len(results)} rows")
                return results
        except pymysql.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise Exception(f"Failed to execute query: {e}")
        finally:
            self.disconnect()

# Global database instance
db = DatabaseConnection()
