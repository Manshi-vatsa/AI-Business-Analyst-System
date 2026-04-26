import logging
import pandas as pd
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AnalysisAgent:
    """
    Analysis Agent - uses pandas to detect patterns and generate insights
    """
    
    def __init__(self):
        pass
    
    def analyze_data(self, data: List[Dict[str, Any]], question: str, steps: List[str]) -> dict:
        """
        Analyze data using pandas and detect specific patterns
        
        Detect:
        - revenue drop
        - top region
        - worst product
        """
        logger.info(f"Analyzing data for question: {question}")
        logger.info(f"Using steps: {steps}")
        
        if not data:
            return {
                "answer": "No data available for analysis",
                "insights": ["No sales data found"]
            }
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        logger.info(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        
        # Ensure numeric columns are properly typed
        if 'revenue' in df.columns:
            df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
        
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        insights = []
        answer = ""
        
        # Analyze based on question type and steps
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["drop", "decrease", "decline", "fall"]):
            insights.extend(self._detect_revenue_drop(df))
            answer = self._generate_drop_answer(df)
            
        elif any(word in question_lower for word in ["region", "area", "location"]):
            insights.extend(self._analyze_regions(df))
            answer = self._generate_region_answer(df)
            
        elif any(word in question_lower for word in ["product", "item", "category"]):
            insights.extend(self._analyze_products(df))
            answer = self._generate_product_answer(df)
            
        elif any(word in question_lower for word in ["total", "sum", "overall"]):
            insights.extend(self._calculate_totals(df))
            answer = self._generate_total_answer(df)
            
        elif any(word in question_lower for word in ["average", "avg", "mean"]):
            insights.extend(self._calculate_averages(df))
            answer = self._generate_average_answer(df)
            
        else:
            # Generic analysis
            insights.extend(self._generic_analysis(df))
            answer = "Analysis completed on sales data"
        
        logger.info(f"Generated {len(insights)} insights")
        return {
            "answer": answer,
            "insights": insights
        }
    
    def _detect_revenue_drop(self, df: pd.DataFrame) -> List[str]:
        """Detect revenue drops between time periods"""
        insights = []
        
        if 'date' in df.columns and 'revenue' in df.columns:
            # Group by month
            df['month'] = df['date'].dt.to_period('M')
            monthly_revenue = df.groupby('month')['revenue'].sum().sort_index(ascending=False)
            
            if len(monthly_revenue) >= 2:
                current_month = monthly_revenue.iloc[0]
                previous_month = monthly_revenue.iloc[1]
                
                if current_month < previous_month:
                    drop_percentage = ((previous_month - current_month) / previous_month) * 100
                    insights.append(f"Revenue dropped by {drop_percentage:.1f}% from previous month")
                    insights.append(f"Previous month: ${previous_month:,.2f}, Current month: ${current_month:,.2f}")
                else:
                    insights.append("Revenue increased compared to previous month")
        
        return insights
    
    def _analyze_regions(self, df: pd.DataFrame) -> List[str]:
        """Analyze regional performance"""
        insights = []
        
        if 'region' in df.columns and 'revenue' in df.columns:
            region_stats = df.groupby('region')['revenue'].agg(['sum', 'count']).sort_values('sum', ascending=False)
            top_region = region_stats.iloc[0]
            
            insights.append(f"Top performing region: {top_region.name} with ${top_region['sum']:,.2f}")
            insights.append(f"{top_region.name} had {top_region['count']} transactions")
            
            if len(region_stats) > 1:
                worst_region = region_stats.iloc[-1]
                insights.append(f"Lowest performing region: {worst_region.name} with ${worst_region['sum']:,.2f}")
        
        return insights
    
    def _analyze_products(self, df: pd.DataFrame) -> List[str]:
        """Analyze product performance"""
        insights = []
        
        if 'product' in df.columns and 'revenue' in df.columns:
            product_stats = df.groupby('product')['revenue'].agg(['sum', 'count']).sort_values('sum', ascending=False)
            top_product = product_stats.iloc[0]
            worst_product = product_stats.iloc[-1]
            
            insights.append(f"Best performing product: {top_product.name} with ${top_product['sum']:,.2f}")
            insights.append(f"Worst performing product: {worst_product.name} with ${worst_product['sum']:,.2f}")
            
            if len(product_stats) > 1:
                insights.append(f"Product performance gap: ${top_product['sum'] - worst_product['sum']:,.2f}")
        
        return insights
    
    def _calculate_totals(self, df: pd.DataFrame) -> List[str]:
        """Calculate total metrics"""
        insights = []
        
        if 'revenue' in df.columns:
            total_revenue = df['revenue'].sum()
            total_transactions = len(df)
            
            insights.append(f"Total revenue: ${total_revenue:,.2f}")
            insights.append(f"Total transactions: {total_transactions:,}")
            
            if total_transactions > 0:
                avg_transaction = total_revenue / total_transactions
                insights.append(f"Average transaction value: ${avg_transaction:.2f}")
        
        return insights
    
    def _calculate_averages(self, df: pd.DataFrame) -> List[str]:
        """Calculate average metrics"""
        insights = []
        
        if 'revenue' in df.columns:
            avg_revenue = df['revenue'].mean()
            median_revenue = df['revenue'].median()
            
            insights.append(f"Average revenue: ${avg_revenue:.2f}")
            insights.append(f"Median revenue: ${median_revenue:.2f}")
            
            # Check for outliers
            q75 = df['revenue'].quantile(0.75)
            q25 = df['revenue'].quantile(0.25)
            insights.append(f"Revenue range (25th-75th percentile): ${q25:.2f} - ${q75:.2f}")
        
        return insights
    
    def _generic_analysis(self, df: pd.DataFrame) -> List[str]:
        """Generic analysis when no specific pattern detected"""
        insights = []
        
        insights.append(f"Analyzed {len(df)} records")
        
        if 'revenue' in df.columns:
            insights.append(f"Revenue range: ${df['revenue'].min():.2f} - ${df['revenue'].max():.2f}")
        
        if 'date' in df.columns:
            date_range = df['date'].max() - df['date'].min()
            insights.append(f"Data covers {date_range.days} days")
        
        return insights
    
    def _generate_drop_answer(self, df: pd.DataFrame) -> str:
        """Generate answer for drop analysis"""
        if 'date' in df.columns and 'revenue' in df.columns:
            df['month'] = df['date'].dt.to_period('M')
            monthly_revenue = df.groupby('month')['revenue'].sum().sort_index(ascending=False)
            
            if len(monthly_revenue) >= 2:
                current_month = monthly_revenue.iloc[0]
                previous_month = monthly_revenue.iloc[1]
                
                if current_month < previous_month:
                    drop_percentage = ((previous_month - current_month) / previous_month) * 100
                    return f"Revenue dropped by {drop_percentage:.1f}% compared to previous month"
        
        return "No significant revenue drop detected"
    
    def _generate_region_answer(self, df: pd.DataFrame) -> str:
        """Generate answer for regional analysis"""
        if 'region' in df.columns and 'revenue' in df.columns:
            top_region = df.groupby('region')['revenue'].sum().idxmax()
            return f"The top performing region is {top_region}"
        return "No regional data available"
    
    def _generate_product_answer(self, df: pd.DataFrame) -> str:
        """Generate answer for product analysis"""
        if 'product' in df.columns and 'revenue' in df.columns:
            top_product = df.groupby('product')['revenue'].sum().idxmax()
            return f"The best performing product is {top_product}"
        return "No product data available"
    
    def _generate_total_answer(self, df: pd.DataFrame) -> str:
        """Generate answer for total analysis"""
        if 'revenue' in df.columns:
            total = df['revenue'].sum()
            return f"Total revenue is ${total:,.2f}"
        return "No revenue data available"
    
    def _generate_average_answer(self, df: pd.DataFrame) -> str:
        """Generate answer for average analysis"""
        if 'revenue' in df.columns:
            avg = df['revenue'].mean()
            return f"Average revenue is ${avg:.2f}"
        return "No revenue data available"
    
    def aggregate_dashboard_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate data for dashboard visualization
        """
        logger.info("=== DASHBOARD AGGREGATION TRACE ===")
        logger.info(f"1. Input data length: {len(data)}")
        logger.info(f"2. Data sample: {data[:2] if data else 'No data'}")
        
        if not data:
            logger.warning("3. No data provided, using enhanced mock data")
            return self._get_enhanced_mock_data()
        
        try:
            # Convert to pandas DataFrame
            df = pd.DataFrame(data)
            logger.info(f"4. DataFrame created with shape: {df.shape}")
            
            # Validate required columns
            required_columns = ['product', 'quantity', 'revenue', 'date', 'region']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"5. Missing required columns: {missing_columns}")
                logger.error(f"6. Available columns: {list(df.columns)}")
                return self._get_enhanced_mock_data()
            
            logger.info(f"5. All required columns present: {required_columns}")
            
            # Ensure proper data types
            if 'revenue' in df.columns:
                df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
                logger.info(f"6. Revenue type converted. Range: {df['revenue'].min()} - {df['revenue'].max()}")
            
            # Handle date column
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                logger.info(f"7. Date column processed: date -> datetime")
            
            # Generate dashboard data
            monthly_sales = self._get_monthly_sales_trend(df)
            region_sales = self._get_region_wise_revenue(df)
            product_sales = self._get_product_performance(df)
            
            dashboard_data = {
                "monthlySales": monthly_sales,
                "regionSales": region_sales,
                "productSales": product_sales
            }
            
            logger.info(f"8. Generated dashboard data:")
            logger.info(f"   - Monthly sales: {len(monthly_sales)} months")
            logger.info(f"   - Region sales: {len(region_sales)} regions")
            logger.info(f"   - Product sales: {len(product_sales)} products")
            
            if monthly_sales:
                logger.info(f"9. Sample monthly data: {monthly_sales[0]}")
            if region_sales:
                logger.info(f"10. Sample region data: {region_sales[0]}")
            if product_sales:
                logger.info(f"11. Sample product data: {product_sales[0]}")
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"12. ERROR in dashboard aggregation: {e}", exc_info=True)
            logger.error(f"13. Exception type: {type(e).__name__}")
            return self._get_enhanced_mock_data()
    
    def _get_enhanced_mock_data(self) -> Dict[str, Any]:
        """
        Return enhanced mock data for dashboard when no database connection
        """
        logger.info("Using enhanced mock data for dashboard")
        
        return {
            "monthlySales": [
                {"month": "2024-01", "revenue": 75000.0},
                {"month": "2024-02", "revenue": 82000.0},
                {"month": "2024-03", "revenue": 68000.0},
                {"month": "2024-04", "revenue": 91000.0},
                {"month": "2024-05", "revenue": 78000.0},
                {"month": "2024-06", "revenue": 85000.0},
                {"month": "2024-07", "revenue": 92000.0},
                {"month": "2024-08", "revenue": 88000.0}
            ],
            "regionSales": [
                {"region": "North", "revenue": 125000.0, "percentage": 35.0},
                {"region": "South", "revenue": 89000.0, "percentage": 25.0},
                {"region": "East", "revenue": 71000.0, "percentage": 20.0},
                {"region": "West", "revenue": 71000.0, "percentage": 20.0}
            ],
            "productSales": [
                {"product": "Laptop", "revenue": 185000.0, "quantity": 185},
                {"product": "Phone", "revenue": 125000.0, "quantity": 250},
                {"product": "Tablet", "revenue": 56000.0, "quantity": 112}
            ]
        }
    
    def _get_monthly_sales_trend(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate monthly sales trend data"""
        if 'date' not in df.columns or 'revenue' not in df.columns:
            return []
        
        # Group by month
        df['month'] = df['date'].dt.to_period('M')
        monthly_sales = df.groupby('month')['revenue'].sum().reset_index()
        monthly_sales['month'] = monthly_sales['month'].dt.strftime('%Y-%m')
        monthly_sales['revenue'] = monthly_sales['revenue'].round(2)
        
        # Sort by month
        monthly_sales = monthly_sales.sort_values('month')
        
        return monthly_sales[['month', 'revenue']].to_dict('records')
    
    def _get_region_wise_revenue(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate region-wise revenue data"""
        if 'region' not in df.columns or 'revenue' not in df.columns:
            return []
        
        # Group by region
        region_sales = df.groupby('region')['revenue'].sum().reset_index()
        region_sales['revenue'] = region_sales['revenue'].round(2)
        
        # Sort by revenue (descending)
        region_sales = region_sales.sort_values('revenue', ascending=False)
        
        return region_sales[['region', 'revenue']].to_dict('records')
    
    def _get_product_performance(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate product performance data"""
        if 'product' not in df.columns or 'revenue' not in df.columns:
            return []
        
        # Group by product
        product_sales = df.groupby('product')['revenue'].sum().reset_index()
        product_sales['revenue'] = product_sales['revenue'].round(2)
        
        # Sort by revenue (descending)
        product_sales = product_sales.sort_values('revenue', ascending=False)
        
        return product_sales[['product', 'revenue']].to_dict('records')
    
    def detect_and_store_insights(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect insights and format for database storage
        
        Returns structured insights for database insertion
        """
        logger.info("Detecting insights for database storage")
        insights = []
        
        try:
            # Detect highest region
            if 'region' in df.columns and 'revenue' in df.columns:
                top_region = df.groupby('region')['revenue'].sum().idxmax()
                top_region_revenue = df.groupby('region')['revenue'].sum().max()
                
                insights.append({
                    "type": "top_region",
                    "message": f"Highest performing region: {top_region}",
                    "value": float(top_region_revenue),
                    "category": "regional_performance"
                })
                
                # Detect lowest region
                worst_region = df.groupby('region')['revenue'].sum().idxmin()
                worst_region_revenue = df.groupby('region')['revenue'].sum().min()
                
                insights.append({
                    "type": "worst_region", 
                    "message": f"Lowest performing region: {worst_region}",
                    "value": float(worst_region_revenue),
                    "category": "regional_performance"
                })
            
            # Detect best and worst products
            if 'product' in df.columns and 'revenue' in df.columns:
                best_product = df.groupby('product')['revenue'].sum().idxmax()
                best_product_revenue = df.groupby('product')['revenue'].sum().max()
                
                insights.append({
                    "type": "best_product",
                    "message": f"Best performing product: {best_product}",
                    "value": float(best_product_revenue),
                    "category": "product_performance"
                })
                
                worst_product = df.groupby('product')['revenue'].sum().idxmin()
                worst_product_revenue = df.groupby('product')['revenue'].sum().min()
                
                insights.append({
                    "type": "worst_product",
                    "message": f"Worst performing product: {worst_product}",
                    "value": float(worst_product_revenue),
                    "category": "product_performance"
                })
            
            # Detect revenue drop
            if 'date' in df.columns and 'revenue' in df.columns:
                df['month'] = df['date'].dt.to_period('M')
                monthly_revenue = df.groupby('month')['revenue'].sum().sort_index(ascending=False)
                
                if len(monthly_revenue) >= 2:
                    current_month = monthly_revenue.iloc[0]
                    previous_month = monthly_revenue.iloc[1]
                    
                    if current_month < previous_month:
                        drop_percentage = ((previous_month - current_month) / previous_month) * 100
                        drop_amount = previous_month - current_month
                        
                        insights.append({
                            "type": "revenue_drop",
                            "message": f"Revenue dropped by {drop_percentage:.1f}% compared to previous month",
                            "value": -round(drop_percentage, 1),
                            "category": "trend_analysis"
                        })
                    else:
                        growth_percentage = ((current_month - previous_month) / previous_month) * 100
                        growth_amount = current_month - previous_month
                        
                        insights.append({
                            "type": "revenue_growth",
                            "message": f"Revenue increased by {growth_percentage:.1f}% compared to previous month",
                            "value": round(growth_percentage, 1),
                            "category": "trend_analysis"
                        })
            
            logger.info(f"Detected {len(insights)} insights for database storage")
            return insights
            
        except Exception as e:
            logger.error(f"Error detecting insights: {e}")
            return []
