import logging
from typing import Dict, List, Any
from db_service import db_service

logger = logging.getLogger(__name__)

class QueryService:
    def __init__(self):
        self.sales_table = "sales"
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """
        Process natural language question using LangChain SQL generation
        """
        try:
            logger.info(f"Processing question: {question}")
            
            # Execute natural language query
            query_result = db_service.execute_natural_language_query(question)
            
            # Generate insights from results
            insights = self._generate_dynamic_insights(query_result)
            
            # Create answer based on results
            answer = self._create_answer(question, query_result)
            
            return {
                "answer": answer,
                "insights": insights,
                "sql_query": query_result.get("sql_query", ""),
                "results": query_result.get("results", [])
            }
        
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                "answer": f"Error processing your question: {str(e)}",
                "insights": [],
                "sql_query": "",
                "results": []
            }
    
    def _create_answer(self, question: str, query_result: Dict[str, Any]) -> str:
        """Create a natural language answer from query results"""
        results = query_result.get("results", [])
        row_count = query_result.get("row_count", 0)
        sql_query = query_result.get("sql_query", "")
        
        if not results:
            return f"No results found for your query: '{question}'"
        
        question_lower = question.lower()
        
        # Handle different types of queries
        if "total sales" in question_lower or "sum" in question_lower:
            if results and results[0]:
                total_value = list(results[0].values())[0]
                return f"Total sales is {total_value}"
        
        elif "average" in question_lower:
            if results and results[0]:
                avg_value = list(results[0].values())[0]
                return f"Average sales is {avg_value}"
        
        elif "count" in question_lower:
            if results and results[0]:
                count_value = list(results[0].values())[0]
                return f"Count is {count_value}"
        
        elif "top products" in question_lower or "best products" in question_lower:
            return f"Found {row_count} top products"
        
        elif "region" in question_lower:
            return f"Found {row_count} regional results"
        
        # Default answer
        return f"Query executed successfully. Found {row_count} results for: '{question}'"
    
    def _generate_dynamic_insights(self, query_result: Dict[str, Any]) -> List[str]:
        """Generate insights based on query results"""
        insights = []
        results = query_result.get("results", [])
        question = query_result.get("question", "")
        
        if not results:
            insights.append("No data available for analysis")
            return insights
        
        question_lower = question.lower()
        
        try:
            # Generate insights based on query type and results
            if "total sales" in question_lower or "sum" in question_lower:
                if results and results[0]:
                    total_value = list(results[0].values())[0]
                    if isinstance(total_value, (int, float)):
                        insights.extend(self._generate_revenue_insights(total_value))
            
            elif "top products" in question_lower or "best products" in question_lower:
                insights.extend(self._generate_product_insights(results))
            
            elif "region" in question_lower:
                insights.extend(self._generate_regional_insights(results))
            
            # General insights
            if len(results) > 1:
                insights.append(f"Analysis based on {len(results)} records")
            
            # Try to find numeric columns for additional insights
            numeric_insights = self._extract_numeric_insights(results)
            insights.extend(numeric_insights)
            
        except Exception as e:
            logger.warning(f"Error generating insights: {e}")
            insights.append("Insights generation partially failed")
        
        return insights
    
    def _generate_revenue_insights(self, total_revenue: float) -> List[str]:
        """Generate insights for revenue-based queries"""
        insights = []
        
        if total_revenue > 100000:
            insights.append("Excellent sales performance - revenue exceeds 100K")
        elif total_revenue > 50000:
            insights.append("Good sales performance - revenue exceeds 50K")
        elif total_revenue > 10000:
            insights.append("Moderate sales performance - revenue exceeds 10K")
        else:
            insights.append("Sales performance needs improvement - revenue below 10K")
        
        return insights
    
    def _generate_product_insights(self, results: List[Dict]) -> List[str]:
        """Generate insights for product-based queries"""
        insights = []
        
        if len(results) >= 1:
            top_product = results[0]
            
            # Try to find product and revenue columns
            product_col = None
            revenue_col = None
            
            for key in top_product.keys():
                if 'product' in key.lower():
                    product_col = key
                elif 'revenue' in key.lower() or 'total' in key.lower():
                    revenue_col = key
            
            if product_col and revenue_col:
                product_name = top_product[product_col]
                product_revenue = top_product[revenue_col]
                insights.append(f"Top performing product: {product_name}")
                insights.append(f"Revenue from top product: {product_revenue}")
            
            insights.append(f"Analysis covers {len(results)} products")
        
        return insights
    
    def _generate_regional_insights(self, results: List[Dict]) -> List[str]:
        """Generate insights for regional queries"""
        insights = []
        
        if len(results) >= 1:
            top_region = results[0]
            
            # Try to find region and revenue columns
            region_col = None
            revenue_col = None
            
            for key in top_region.keys():
                if 'region' in key.lower():
                    region_col = key
                elif 'revenue' in key.lower() or 'total' in key.lower():
                    revenue_col = key
            
            if region_col and revenue_col:
                region_name = top_region[region_col]
                region_revenue = top_region[revenue_col]
                insights.append(f"{region_name} region contributes highest revenue")
                insights.append(f"Top region revenue: {region_revenue}")
            
            insights.append(f"Analysis covers {len(results)} regions")
        
        return insights
    
    def _extract_numeric_insights(self, results: List[Dict]) -> List[str]:
        """Extract insights from numeric columns"""
        insights = []
        
        if not results:
            return insights
        
        try:
            # Find numeric columns
            numeric_columns = []
            if results:
                for key, value in results[0].items():
                    if isinstance(value, (int, float)):
                        numeric_columns.append(key)
            
            if numeric_columns:
                insights.append(f"Found {len(numeric_columns)} numeric columns for analysis")
                
                # Generate range insights for the first numeric column
                if len(numeric_columns) > 0:
                    col_name = numeric_columns[0]
                    values = [r.get(col_name, 0) for r in results if r.get(col_name) is not None]
                    
                    if values:
                        insights.append(f"{col_name} range: {min(values)} - {max(values)}")
                        insights.append(f"Average {col_name}: {sum(values)/len(values):.2f}")
        
        except Exception as e:
            logger.warning(f"Error extracting numeric insights: {e}")
        
        return insights
    
    def get_database_status(self) -> Dict[str, Any]:
        """Get database status and information"""
        try:
            return db_service.get_database_info()
        except Exception as e:
            logger.error(f"Error getting database status: {e}")
            return {
                "connected": False,
                "error": str(e)
            }

# Global service instance
query_service = QueryService()
