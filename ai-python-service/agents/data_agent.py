import logging
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)

class DataAgent:
    """
    Data Agent - handles data retrieval operations
    """
    
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def fetch_sales_data(self) -> list:
        """
        Fetch all sales data from database
        """
        try:
            connection = self.db_connection.connect()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM sales")
                results = cursor.fetchall()
                logger.info(f"Fetched {len(results)} sales records")
                return results
        except Exception as e:
            logger.error(f"Error fetching sales data: {e}")
            return []
