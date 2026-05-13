import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class IntelligentAnalysis:
    """
    Intelligent Analysis Service - generates meaningful business insights from SQL results
    """
    
    def __init__(self):
        self.numeric_keywords = ['revenue', 'sales', 'amount', 'price', 'cost', 'profit', 'quantity', 'count', 'total']
        self.date_keywords = ['date', 'time', 'created', 'updated', 'timestamp']
        self.category_keywords = ['product', 'region', 'category', 'type', 'status', 'name']
        
    def analyze_data_intelligently(self, data: List[Dict[str, Any]], question: str) -> Dict[str, Any]:
        """
        Generate intelligent business insights from data
        
        Args:
            data: SQL query results
            question: Original user question
            
        Returns:
            Dict with 'answer' and 'insights' keys
        """
        logger.info(f"Starting intelligent analysis for {len(data)} records")
        
        if not data:
            return {
                "answer": "No data found for the query",
                "insights": ["No records available for analysis"]
            }
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        logger.info(f"DataFrame created with {len(df)} rows and {len(df.columns)} columns")
        
        # Detect column types
        column_info = self._detect_column_types(df)
        logger.info(f"Detected columns: {column_info}")
        
        # Generate insights based on data characteristics
        insights = self._generate_comprehensive_insights(df, column_info, question)
        
        # Generate meaningful answer
        answer = self._generate_meaningful_answer(df, column_info, question, insights)
        
        logger.info(f"Generated {len(insights)} insights and meaningful answer")
        
        return {
            "answer": answer,
            "insights": insights
        }
    
    def _detect_column_types(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Detect column types dynamically
        """
        column_info = {
            'numeric': [],
            'date': [],
            'categorical': [],
            'text': []
        }
        
        for column in df.columns:
            column_lower = column.lower()
            
            # Try to convert to numeric
            numeric_series = pd.to_numeric(df[column], errors='coerce')
            if not numeric_series.isna().all():
                column_info['numeric'].append(column)
                continue
            
            # Try to convert to datetime
            date_series = pd.to_datetime(df[column], errors='coerce')
            if not date_series.isna().all():
                column_info['date'].append(column)
                continue
            
            # Check if categorical (low cardinality)
            unique_count = df[column].nunique()
            if unique_count <= 20 and unique_count < len(df) * 0.5:
                column_info['categorical'].append(column)
            else:
                column_info['text'].append(column)
        
        return column_info
    
    def _generate_comprehensive_insights(self, df: pd.DataFrame, column_info: Dict[str, List[str]], question: str) -> List[str]:
        """
        Generate comprehensive insights from the data
        """
        insights = []
        
        # Dataset summary
        insights.append(f"Dataset contains {len(df)} records")
        
        # Numeric analysis
        if column_info['numeric']:
            insights.extend(self._analyze_numeric_columns(df, column_info['numeric']))
        
        # Categorical analysis
        if column_info['categorical']:
            insights.extend(self._analyze_categorical_columns(df, column_info['categorical']))
        
        # Date analysis
        if column_info['date']:
            insights.extend(self._analyze_date_columns(df, column_info['date']))
        
        # Cross-analysis
        if len(column_info['numeric']) > 0 and len(column_info['categorical']) > 0:
            insights.extend(self._analyze_numeric_by_category(df, column_info['numeric'], column_info['categorical']))
        
        return insights[:6]  # Limit to 6 most relevant insights
    
    def _analyze_numeric_columns(self, df: pd.DataFrame, numeric_columns: List[str]) -> List[str]:
        """
        Analyze numeric columns for specific, data-driven insights
        """
        insights = []
        
        for column in numeric_columns:
            series = pd.to_numeric(df[column], errors='coerce').dropna()
            
            if len(series) == 0:
                continue
            
            # Basic statistics
            mean_val = series.mean()
            max_val = series.max()
            min_val = series.min()
            median_val = series.median()
            
            # Generate specific, data-driven insights
            if column.lower() in ['revenue', 'sales', 'amount', 'price']:
                insights.append(f"Highest revenue is ${max_val:,.2f}")
                insights.append(f"Lowest revenue is ${min_val:,.2f}")
                insights.append(f"Average revenue is around ${mean_val:,.2f}")
                
                # Add performance insight
                if max_val > mean_val * 2:
                    insights.append(f"Revenue shows high variation with peak at ${max_val:,.2f}")
                elif min_val < mean_val * 0.5:
                    insights.append(f"Some revenue significantly below average at ${min_val:,.2f}")
                    
            elif 'count' in column.lower() or 'total' in column.lower():
                insights.append(f"Highest count is {int(max_val)}")
                insights.append(f"Lowest count is {int(min_val)}")
                insights.append(f"Average count is around {int(mean_val)}")
            else:
                insights.append(f"Highest {column} is {max_val:,.2f}")
                insights.append(f"Lowest {column} is {min_val:,.2f}")
                insights.append(f"Average {column} is around {mean_val:,.2f}")
            
            # Variance and distribution insights
            if len(series) > 1:
                std_val = series.std()
                if std_val > mean_val * 0.5:  # High variance
                    insights.append(f"{column} shows high variability in performance")
                elif std_val < mean_val * 0.1:  # Low variance
                    insights.append(f"{column} shows consistent performance")
                
                # Add trend insight if we have enough data points
                if len(series) >= 3:
                    if series.iloc[-1] > series.iloc[0]:  # Increasing trend
                        insights.append(f"{column} shows upward trend")
                    elif series.iloc[-1] < series.iloc[0]:  # Decreasing trend
                        insights.append(f"{column} shows downward trend")
        
        return insights
    
    def _analyze_categorical_columns(self, df: pd.DataFrame, categorical_columns: List[str]) -> List[str]:
        """
        Analyze categorical columns for specific, data-driven insights
        """
        insights = []
        
        for column in categorical_columns:
            value_counts = df[column].value_counts()
            
            if len(value_counts) == 0:
                continue
            
            # Top performer
            top_category = value_counts.index[0]
            top_count = value_counts.iloc[0]
            top_percentage = (top_count / len(df)) * 100
            
            if column.lower() in ['product', 'item']:
                insights.append(f"Top product is {top_category} with {top_count} occurrences")
                if top_percentage > 50:
                    insights.append(f"{top_category} dominates with {top_percentage:.1f}% market share")
            elif column.lower() in ['region', 'area', 'location']:
                insights.append(f"Best performing region is {top_category} with {top_count} records")
                if top_percentage > 40:
                    insights.append(f"{top_category} leads with {top_percentage:.1f}% of total activity")
            else:
                insights.append(f"Most common {column} is {top_category} ({top_count} occurrences)")
                if top_percentage > 50:
                    insights.append(f"{top_category} represents {top_percentage:.1f}% of all records")
            
            # Distribution insight
            if len(value_counts) > 1:
                second_best = value_counts.iloc[1]
                second_percentage = (second_best / len(df)) * 100
                
                # Competitive analysis
                if top_count - second_best < top_count * 0.2:  # Close competition
                    insights.append(f"Tight competition between {top_category} and {second_best}")
                elif top_count > second_best * 3:  # Dominant leader
                    insights.append(f"{top_category} significantly outperforms competitors")
                
                # Diversity insight
                if len(value_counts) >= 5:
                    insights.append(f"Diverse {column} distribution with {len(value_counts)} different categories")
                elif len(value_counts) == 2:
                    insights.append(f"Concentrated {column} market with two main categories")
        
        return insights
    
    def _analyze_date_columns(self, df: pd.DataFrame, date_columns: List[str]) -> List[str]:
        """
        Analyze date columns for insights
        """
        insights = []
        
        for column in date_columns:
            date_series = pd.to_datetime(df[column], errors='coerce').dropna()
            
            if len(date_series) == 0:
                continue
            
            # Date range
            min_date = date_series.min()
            max_date = date_series.max()
            
            if min_date != max_date:
                date_range = (max_date - min_date).days
                insights.append(f"Data spans {date_range} days from {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
                
                # Recent activity
                recent_cutoff = max_date - timedelta(days=30)
                recent_count = (date_series >= recent_cutoff).sum()
                if recent_count > 0:
                    insights.append(f"{recent_count} records from last 30 days")
        
        return insights
    
    def _analyze_numeric_by_category(self, df: pd.DataFrame, numeric_columns: List[str], categorical_columns: List[str]) -> List[str]:
        """
        Analyze numeric values by categories
        """
        insights = []
        
        for numeric_col in numeric_columns:
            for cat_col in categorical_columns:
                try:
                    numeric_series = pd.to_numeric(df[numeric_col], errors='coerce')
                    
                    # Group by category and find best performer
                    grouped = df.groupby(cat_col)[numeric_col].apply(lambda x: pd.to_numeric(x, errors='coerce').mean())
                    grouped = grouped.dropna()
                    
                    if len(grouped) > 0:
                        best_category = grouped.idxmax()
                        best_value = grouped.max()
                        
                        if numeric_col.lower() in ['revenue', 'sales', 'amount', 'price']:
                            insights.append(f"Best {cat_col} by {numeric_col}: {best_category} (${best_value:,.2f})")
                        else:
                            insights.append(f"Best {cat_col} by {numeric_col}: {best_category} ({best_value:.2f})")
                
                except Exception as e:
                    logger.warning(f"Error analyzing {numeric_col} by {cat_col}: {e}")
                    continue
        
        return insights
    
    def _generate_meaningful_answer(self, df: pd.DataFrame, column_info: Dict[str, List[str]], question: str, insights: List[str]) -> str:
        """
        Generate a meaningful business answer based on the analysis
        """
        question_lower = question.lower()
        
        # Single value responses
        if len(df) == 1:
            return self._generate_single_value_answer(df.iloc[0], column_info)
        
        # Multiple rows responses
        if len(df) > 1:
            return self._generate_multi_row_answer(df, column_info, question_lower, insights)
        
        return "Analysis completed on the data"
    
    def _generate_single_value_answer(self, row: pd.Series, column_info: Dict[str, List[str]]) -> str:
        """
        Generate answer for single value results (2-4 lines, business-friendly)
        """
        if column_info['numeric']:
            numeric_col = column_info['numeric'][0]
            value = row[numeric_col]
            
            if numeric_col.lower() in ['revenue', 'sales', 'amount', 'price']:
                return f"Total {numeric_col} is {value:,.2f}, indicating overall revenue performance.\nThis metric provides a comprehensive view of the business's financial results.\nThe value reflects the complete aggregate for the specified time period."
            elif 'total' in numeric_col.lower() or 'sum' in numeric_col.lower():
                return f"Total {numeric_col} is {value:,.2f}, showing the complete aggregate value.\nThis represents the sum of all records in the dataset.\nThe metric provides insight into overall business performance."
            elif 'count' in numeric_col.lower():
                return f"Total count is {int(value)}, representing the total number of records.\nThis metric shows the volume of data analyzed.\nThe count helps understand the scale of the business operations."
            else:
                return f"Total {numeric_col} is {value:,.2f}, showing the current metric value.\nThis provides a quantitative measure of business performance.\nThe value helps track key performance indicators."
        
        return f"Analysis shows 1 record with the specified criteria.\nThis represents a focused result set for the query.\nThe single record provides specific information for the requested analysis."
    
    def _generate_multi_row_answer(self, df: pd.DataFrame, column_info: Dict[str, List[str]], question_lower: str, insights: List[str]) -> str:
        """
        Generate answer for multiple row results (2-4 lines, business-friendly)
        """
        # Extract key metrics from insights
        highest_value = None
        lowest_value = None
        average_value = None
        trend_info = ""
        top_performer = None
        
        for insight in insights:
            if "Highest" in insight and ("revenue" in insight.lower() or "sales" in insight.lower()):
                highest_value = insight
            elif "Lowest" in insight and ("revenue" in insight.lower() or "sales" in insight.lower()):
                lowest_value = insight
            elif "Average" in insight and ("revenue" in insight.lower() or "sales" in insight.lower()):
                average_value = insight
            elif "spans" in insight and "days" in insight:
                trend_info = insight
            elif ("Top" in insight or "Best" in insight) and ("product" in insight.lower() or "region" in insight.lower()):
                top_performer = insight
        
        # Generate contextual answer based on question type
        if "recent" in question_lower or "latest" in question_lower:
            if highest_value and lowest_value:
                high_num = self._extract_number(highest_value)
                low_num = self._extract_number(lowest_value)
                return f"The latest {len(df)} sales records show fluctuating revenue, with the highest sale reaching {high_num} while some entries are significantly lower at {low_num}.\nThis indicates inconsistent performance patterns in recent business activity.\nThe variation suggests opportunities for performance optimization and revenue stabilization."
            else:
                return f"The latest {len(df)} records show varying performance patterns across the analyzed time period.\nThe data reveals different levels of business activity and performance metrics.\nThis variation provides insights into business dynamics and potential areas for improvement."
        
        # For "total" or "sum" queries
        elif "total" in question_lower or "sum" in question_lower or "overall" in question_lower:
            if highest_value and average_value:
                high_num = self._extract_number(highest_value)
                avg_num = self._extract_number(average_value)
                return f"Total analysis shows significant variation with peak values at {high_num} and average performance around {avg_num}.\nThis indicates diverse business metrics across different categories or time periods.\nThe variation helps identify areas of strength and opportunities for improvement."
            else:
                return f"Analysis of {len(df)} records reveals comprehensive performance metrics across the specified categories.\nThe data provides a complete view of business performance and operational results.\nThese insights support data-driven decision making and strategic planning."
        
        # For "top" or "best" queries
        elif "top" in question_lower or "best" in question_lower:
            if top_performer:
                return f"Analysis identifies clear performance leaders with {top_performer.lower()}.\nThis shows strong competitive positioning in key business areas.\nThe top performers demonstrate best practices that can be leveraged across the organization."
            else:
                return f"Performance analysis reveals top performers across {len(df)} categories with measurable business impact.\nThe analysis highlights areas of excellence and competitive advantage.\nThese insights support strategic decision making and resource allocation."
        
        # General multi-row answer
        if column_info['numeric'] and highest_value and lowest_value:
            high_num = self._extract_number(highest_value)
            low_num = self._extract_number(lowest_value)
            if average_value:
                avg_num = self._extract_number(average_value)
                return f"Analysis of {len(df)} records shows performance ranging from {low_num} to {high_num}, averaging {avg_num}.\nThis indicates varied business outcomes across different segments or time periods.\nThe range and average provide context for performance evaluation and goal setting."
            else:
                return f"Analysis of {len(df)} records shows performance ranging from {low_num} to {high_num}.\nThis indicates significant variation in business metrics and operational results.\nThe variation highlights both strengths and areas for improvement."
        
        elif column_info['categorical'] and top_performer:
            return f"Analysis reveals {top_performer.lower()}, demonstrating clear performance patterns across business categories.\nThis provides insights into market dynamics and competitive positioning.\nThe patterns support strategic planning and operational decisions."
        
        else:
            return f"Analysis of {len(df)} records provides comprehensive insights into business performance and trends.\nThe data reveals important patterns and relationships in business operations.\nThese insights support informed decision making and strategic planning."
    
    def _extract_number(self, text: str) -> str:
        """
        Extract numeric value from insight text
        """
        import re
        # Look for patterns like "$5,200.00" or "5200.00"
        match = re.search(r'\$?([0-9,]+\.?\d*)', text)
        if match:
            number = match.group(1)
            if '$' in text:
                return f"${number}"
            return number
        return text
