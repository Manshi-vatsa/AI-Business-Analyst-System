import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ReportAgent:
    """
    Report Agent - converts insights into human-readable answers
    """
    
    def __init__(self):
        pass
    
    def generate_report(self, analysis_result: dict) -> dict:
        """
        Convert insights into human-readable answer
        
        Input: analysis_result with 'answer' and 'insights'
        Output: formatted human-readable response
        """
        logger.info("Generating human-readable report")
        
        answer = analysis_result.get("answer", "No analysis available")
        insights = analysis_result.get("insights", [])
        
        # Format the response to be more natural and conversational
        formatted_answer = self._format_answer(answer, insights)
        
        # Create additional context from insights
        additional_context = self._extract_context(insights)
        
        result = {
            "answer": formatted_answer,
            "insights": insights,
            "context": additional_context
        }
        
        logger.info(f"Generated report with {len(insights)} insights")
        return result
    
    def _format_answer(self, answer: str, insights: List[str]) -> str:
        """
        Format the answer to be more natural and conversational
        """
        if not answer or answer == "No analysis available":
            return "I'm sorry, but I couldn't analyze the data to answer your question."
        
        # Make the answer more conversational
        formatted = answer
        
        # Add context from insights if available
        if insights and len(insights) > 1:
            # If we have multiple insights, make it more comprehensive
            if "total revenue" in formatted.lower():
                formatted += f" Based on the analysis, I found {len(insights)} key insights about your sales data."
            elif "top performing" in formatted.lower() or "best performing" in formatted.lower():
                formatted += f" I also analyzed {len(insights)} different aspects to give you a complete picture."
            elif "dropped" in formatted.lower() or "decrease" in formatted.lower():
                formatted += f" Here are {len(insights)} important findings about the revenue changes."
        elif insights and len(insights) == 1:
            formatted += f" Here's the key insight I found."
        
        return formatted
    
    def _extract_context(self, insights: List[str]) -> Dict[str, Any]:
        """
        Extract structured context from insights
        """
        context = {
            "key_metrics": [],
            "trends": [],
            "recommendations": []
        }
        
        for insight in insights:
            insight_lower = insight.lower()
            
            # Extract key metrics
            if any(metric in insight_lower for metric in ["total revenue", "average revenue", "total transactions"]):
                context["key_metrics"].append(insight)
            
            # Extract trends
            elif any(trend in insight_lower for trend in ["dropped", "increased", "decrease", "decline", "growth"]):
                context["trends"].append(insight)
            
            # Extract recommendations (if any)
            elif any(rec in insight_lower for rec in ["recommend", "suggest", "should", "consider"]):
                context["recommendations"].append(insight)
        
        # If no specific categories, add to general insights
        if not context["key_metrics"] and not context["trends"] and not context["recommendations"]:
            context["general"] = insights
        
        return context
    
    def format_for_dashboard(self, analysis_result: dict) -> dict:
        """
        Format results specifically for dashboard display
        """
        logger.info("Formatting results for dashboard")
        
        answer = analysis_result.get("answer", "")
        insights = analysis_result.get("insights", [])
        
        # Extract specific metrics for dashboard
        dashboard_data = {
            "summary": answer,
            "metrics": [],
            "charts": []
        }
        
        # Parse insights for dashboard metrics
        for insight in insights:
            if "total revenue" in insight.lower():
                # Extract numeric value for charts
                import re
                numbers = re.findall(r'\$?[\d,]+\.?\d*', insight)
                if numbers:
                    dashboard_data["metrics"].append({
                        "label": "Total Revenue",
                        "value": numbers[0],
                        "type": "currency"
                    })
            
            elif "top performing" in insight.lower() or "best performing" in insight.lower():
                dashboard_data["metrics"].append({
                    "label": "Top Performer",
                    "value": insight,
                    "type": "text"
                })
            
            elif "dropped" in insight.lower() or "decrease" in insight.lower():
                dashboard_data["metrics"].append({
                    "label": "Trend",
                    "value": insight,
                    "type": "trend"
                })
        
        return dashboard_data
