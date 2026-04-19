import logging
from typing import Dict, List, Any, Optional
from db_service import db_service

logger = logging.getLogger(__name__)

class InsightsService:
    """
    Service for generating automatic insights from sales data
    """
    
    def __init__(self):
        pass
    
    def analyze_sales_data(self) -> Dict[str, Any]:
        """
        Analyze sales data and return comprehensive insights
        """
        try:
            insights = {}
            
            # Get all sales data
            all_sales_query = "SELECT * FROM sales"
            all_sales = db_service.execute_query(all_sales_query)
            
            if not all_sales:
                return {"error": "No sales data available for analysis"}
            
            # Analyze total revenue
            total_revenue_query = "SELECT SUM(revenue) as total_revenue FROM sales"
            total_revenue_result = db_service.execute_query(total_revenue_query)
            total_revenue = total_revenue_result[0]['total_revenue'] if total_revenue_result else 0
            
            insights['total_revenue'] = float(total_revenue)
            
            # Find highest region by revenue
            highest_region_query = """
                SELECT region, SUM(revenue) as region_revenue 
                FROM sales 
                GROUP BY region 
                ORDER BY region_revenue DESC 
                LIMIT 1
            """
            highest_region_result = db_service.execute_query(highest_region_query)
            if highest_region_result:
                insights['highest_region'] = {
                    'region': highest_region_result[0]['region'],
                    'revenue': float(highest_region_result[0]['region_revenue'])
                }
            
            # Find lowest product by revenue
            lowest_product_query = """
                SELECT product, SUM(revenue) as product_revenue 
                FROM sales 
                GROUP BY product 
                ORDER BY product_revenue ASC 
                LIMIT 1
            """
            lowest_product_result = db_service.execute_query(lowest_product_query)
            if lowest_product_result:
                insights['lowest_product'] = {
                    'product': lowest_product_result[0]['product'],
                    'revenue': float(lowest_product_result[0]['product_revenue'])
                }
            
            # Additional insights
            insights['total_sales_count'] = len(all_sales)
            insights['average_sale'] = total_revenue / len(all_sales) if all_sales else 0
            
            # Get revenue by region for breakdown
            region_breakdown_query = """
                SELECT region, SUM(revenue) as revenue, COUNT(*) as count 
                FROM sales 
                GROUP BY region 
                ORDER BY revenue DESC
            """
            region_breakdown = db_service.execute_query(region_breakdown_query)
            insights['region_breakdown'] = region_breakdown
            
            # Get revenue by product for breakdown
            product_breakdown_query = """
                SELECT product, SUM(revenue) as revenue, COUNT(*) as count 
                FROM sales 
                GROUP BY product 
                ORDER BY revenue DESC
            """
            product_breakdown = db_service.execute_query(product_breakdown_query)
            insights['product_breakdown'] = product_breakdown
            
            # Performance indicators
            insights['performance_indicators'] = self._generate_performance_indicators(total_revenue, all_sales)
            
            logger.info(f"Generated insights: {insights}")
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing sales data: {e}")
            return {"error": f"Failed to analyze sales data: {str(e)}"}
    
    def _generate_performance_indicators(self, total_revenue: float, all_sales: List[Dict]) -> List[str]:
        """Generate performance indicators based on sales data"""
        indicators = []
        
        # Revenue performance
        if total_revenue > 100000:
            indicators.append("Excellent performance - revenue exceeds 100K")
        elif total_revenue > 50000:
            indicators.append("Good performance - revenue exceeds 50K")
        elif total_revenue > 10000:
            indicators.append("Moderate performance - revenue exceeds 10K")
        else:
            indicators.append("Performance needs improvement - revenue below 10K")
        
        # Data volume indicators
        if len(all_sales) > 1000:
            indicators.append("High data volume - over 1000 sales records")
        elif len(all_sales) > 500:
            indicators.append("Medium data volume - 500-1000 sales records")
        elif len(all_sales) > 100:
            indicators.append("Low data volume - 100-500 sales records")
        else:
            indicators.append("Very low data volume - under 100 sales records")
        
        return indicators
    
    def store_insights(self, insights: Dict[str, Any]) -> bool:
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
            for insight_type, insight_data in insights.items():
                if insight_type not in ['error'] and isinstance(insight_data, (dict, list, str, int, float)):
                    import json
                    insert_query = """
                        INSERT INTO insights (insight_type, insight_data) 
                        VALUES (%s, %s)
                    """
                    
                    # Convert to JSON for complex data
                    if isinstance(insight_data, (dict, list)):
                        insight_json = json.dumps(insight_data)
                    else:
                        insight_json = str(insight_data)
                    
                    params = (insight_type, insight_json)
                    db_service.execute_query(insert_query, params)
            
            logger.info("Insights stored successfully in MySQL")
            return True
            
        except Exception as e:
            logger.error(f"Error storing insights: {e}")
            return False

# Global insights service instance
insights_service = InsightsService()
