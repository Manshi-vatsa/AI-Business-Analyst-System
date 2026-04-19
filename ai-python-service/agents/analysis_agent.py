import logging

logger = logging.getLogger(__name__)

class AnalysisAgent:
    """
    Analysis Agent - processes data and generates insights
    """
    
    def __init__(self):
        pass
    
    def analyze_data(self, data: list, question: str) -> dict:
        """
        Analyze sales data and generate insights
        """
        logger.info(f"Analyzing data for question: {question}")
        
        if not data:
            return {
                "answer": "No data available for analysis",
                "insights": ["No sales data found"]
            }
        
        # Basic analysis
        total_records = len(data)
        insights = []
        
        # Generate insights based on question
        question_lower = question.lower()
        
        if "total" in question_lower and ("sales" in question_lower or "revenue" in question_lower):
            total_revenue = sum(float(record.get('revenue', 0)) for record in data)
            insights.append(f"Total revenue: ${total_revenue:,.2f}")
            answer = f"Total sales revenue is ${total_revenue:,.2f}"
        
        elif "average" in question_lower:
            total_revenue = sum(float(record.get('revenue', 0)) for record in data)
            avg_revenue = total_revenue / total_records if total_records > 0 else 0
            insights.append(f"Average revenue: ${avg_revenue:,.2f}")
            answer = f"Average sales revenue is ${avg_revenue:,.2f}"
        
        elif "count" in question_lower:
            insights.append(f"Total sales records: {total_records}")
            answer = f"Found {total_records} sales records"
        
        else:
            # Generic analysis
            insights.append(f"Analyzed {total_records} sales records")
            answer = f"Analysis completed on {total_records} records"
        
        return {
            "answer": answer,
            "insights": insights
        }
