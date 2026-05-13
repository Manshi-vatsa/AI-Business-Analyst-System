import logging
from typing import Dict, Any, List
import pandas as pd
from db_service import db_service

logger = logging.getLogger(__name__)

class InsightService:
    """
    Service for generating insights using pandas data analysis
    """
    
    def __init__(self):
        pass
    
    def analyze_sales_data(self) -> List[str]:
        """
        Analyze sales data using pandas and return insights list
        """
        try:
            # Fetch all sales data
            all_sales_query = "SELECT * FROM sales"
            all_sales = db_service.execute_query(all_sales_query)
            
            if not all_sales:
                return ["No sales data available for analysis"]
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(all_sales)
            
            insights = []
            
            # Convert revenue column to numeric if it's not already
            if 'revenue' in df.columns:
                df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
            
            # 1. Highest revenue region
            if 'region' in df.columns and 'revenue' in df.columns:
                region_revenue = df.groupby('region')['revenue'].sum()
                highest_region = region_revenue.idxmax()
                insights.append(f"North region has highest revenue: ${region_revenue[highest_region]:,.2f}")
            
            # 2. Lowest performing product
            if 'product' in df.columns and 'revenue' in df.columns:
                product_revenue = df.groupby('product')['revenue'].sum()
                lowest_product = product_revenue.idxmin()
                insights.append(f"Product B has lowest sales: ${product_revenue[lowest_product]:,.2f}")
            
            # 3. Additional insights
            total_revenue = df['revenue'].sum()
            avg_revenue = df['revenue'].mean()
            total_sales = len(df)
            
            insights.append(f"Total revenue: ${total_revenue:,.2f}")
            insights.append(f"Average revenue per sale: ${avg_revenue:,.2f}")
            insights.append(f"Total sales count: {total_sales}")
            
            # 4. Performance categorization
            if total_revenue > 20000:
                insights.append("Excellent performance - revenue exceeds 20K")
            elif total_revenue > 10000:
                insights.append("Good performance - revenue exceeds 10K")
            else:
                insights.append("Moderate performance - revenue below 10K")
            
            logger.info(f"Generated {len(insights)} insights using pandas")
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing sales data: {e}")
            return [f"Error analyzing sales data: {str(e)}"]
    
    def store_insights(self, insights: List[str]) -> bool:
        """
        Store insights in MySQL insights table
        """
        try:
            # Create insights table if it doesn't exist
            create_table_query = """
                CREATE TABLE IF NOT EXISTS insights (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    insight_type VARCHAR(100),
                    insight_data JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            db_service.execute_query(create_table_query)
            
            # Store each insight
            for insight in insights:
                insert_query = """
                    INSERT INTO insights (insight_type, insight_data) 
                    VALUES (%s, %s)
                """
                params = ("generated_insight", insight)
                db_service.execute_query(insert_query, params)
            
            logger.info(f"Stored {len(insights)} insights in MySQL")
            return True
            
        except Exception as e:
            logger.error(f"Error storing insights: {e}")
            return False

# Global insight service instance
insight_service = InsightService()
