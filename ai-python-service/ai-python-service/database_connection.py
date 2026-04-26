"""
==========================================
PRODUCTION-READY DATABASE CONNECTION
==========================================
Clean, production-ready database connection module for FastAPI
"""

import os
import logging
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    Production-ready database connection with proper error handling
    """
    
    def __init__(self):
        self.config = self._get_config()
        self.max_retries = int(os.getenv('DB_MAX_RETRIES', 3))
        self.retry_delay = int(os.getenv('DB_RETRY_DELAY', 2))
        self.connection = None
        
        logger.info(f"DatabaseConnection initialized")
        logger.info(f"Config: {self.config['host']}:{self.config['port']}/{self.config['database']}")
    
    def _get_config(self) -> Dict[str, Any]:
        """Get database configuration from environment variables"""
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'ai_analytics'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'Manshi@263'),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True,
            'raise_on_warnings': True,
            'sql_mode': 'TRADITIONAL',
            'connect_timeout': 60,
            'read_timeout': 30,
            'write_timeout': 30
        }
    
    def connect(self) -> bool:
        """
        Establish database connection with retry mechanism
        """
        logger.info("=== DATABASE CONNECTION ATTEMPT ===")
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries}")
                
                self.connection = mysql.connector.connect(**self.config)
                
                # Test connection
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                
                logger.info("✅ Database connection successful")
                logger.info(f"   Server: {self.connection.server_info}")
                logger.info(f"   Database: {self.config['database']}")
                logger.info(f"   User: {self.config['user']}")
                
                return True
                
            except Error as e:
                logger.error(f"❌ Connection failed (attempt {attempt + 1}): {e}")
                logger.error(f"   Error code: {e.errno}")
                logger.error(f"   SQL State: {e.sqlstate}")
                
                if attempt < self.max_retries - 1:
                    logger.info(f"   Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("❌ Max retries reached")
                    return False
        
        return False
    
    def disconnect(self):
        """Safely close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("✅ Database connection closed")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute SQL query with proper error handling
        """
        logger.info("=== QUERY EXECUTION ===")
        logger.info(f"Query: {query}")
        if params:
            logger.info(f"Params: {params}")
        
        if not self.connection or not self.connection.is_connected():
            logger.error("❌ No database connection")
            raise Exception("Database not connected")
        
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            # Fetch results
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                logger.info(f"✅ Query executed successfully. Rows returned: {len(results)}")
                
                # Log sample result
                if results:
                    logger.info(f"   Sample result: {results[0]}")
                
                return results
            else:
                # For INSERT, UPDATE, DELETE
                self.connection.commit()
                affected_rows = cursor.rowcount
                logger.info(f"✅ Query executed successfully. Rows affected: {affected_rows}")
                return [{'affected_rows': affected_rows}]
                
        except Error as e:
            logger.error(f"❌ Query execution failed: {e}")
            logger.error(f"   Error code: {e.errno}")
            logger.error(f"   SQL State: {e.sqlstate}")
            self.connection.rollback()
            raise Exception(f"Query execution failed: {str(e)}")
        finally:
            if cursor:
                cursor.close()
                logger.info("✅ Cursor closed")
    
    def test_connection(self) -> bool:
        """
        Test database connection without affecting main connection
        """
        logger.info("=== CONNECTION TEST ===")
        
        try:
            test_config = self.config.copy()
            test_connection = mysql.connector.connect(**test_config)
            
            cursor = test_connection.cursor()
            cursor.execute("SELECT VERSION() as version")
            result = cursor.fetchone()
            cursor.close()
            test_connection.close()
            
            logger.info(f"✅ Connection test successful")
            logger.info(f"   MySQL Version: {result['version']}")
            return True
            
        except Error as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False
    
    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get current connection information
        """
        if not self.connection or not self.connection.is_connected():
            return {'status': 'disconnected'}
        
        return {
            'status': 'connected',
            'host': self.config['host'],
            'port': self.config['port'],
            'database': self.config['database'],
            'user': self.config['user'],
            'server_info': self.connection.server_info
        }
