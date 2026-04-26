import logging
import pandas as pd
from typing import List, Dict, Any
from agents.planner_agent import PlannerAgent
from agents.data_agent import DataAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent

logger = logging.getLogger(__name__)

class AgentPipeline:
    """
    Agent Pipeline - orchestrates the flow: Planner → Data → Analysis → Report
    """
    
    def __init__(self):
        self.planner_agent = PlannerAgent()
        self.data_agent = DataAgent()
        self.analysis_agent = AnalysisAgent()
        self.report_agent = ReportAgent()
        
        logger.info("Agent Pipeline initialized with all agents")
    
    def process_query(self, question: str) -> Dict[str, Any]:
        """
        Process user question through the complete agent pipeline
        
        Flow: Planner → Data → Analysis → Report
        
        Returns:
        {
            "answer": "...",
            "insights": ["..."],
            "steps_executed": ["..."],
            "agent_logs": ["..."]
        }
        """
        logger.info(f"Starting pipeline processing for question: {question}")
        
        result = {
            "answer": "",
            "insights": [],
            "steps_executed": [],
            "agent_logs": []
        }
        
        try:
            # Step 1: Planner Agent - Generate execution steps
            logger.info("=== STEP 1: PLANNER AGENT ===")
            result["agent_logs"].append("Planner Agent: Generating execution steps")
            
            steps = self.planner_agent.plan_query(question)
            result["steps_executed"] = steps
            logger.info(f"Planner generated steps: {steps}")
            result["agent_logs"].append(f"Planner Agent: Generated {len(steps)} execution steps")
            
            # Step 2: Data Agent - Get data based on steps
            logger.info("=== STEP 2: DATA AGENT ===")
            result["agent_logs"].append("Data Agent: Converting natural language to SQL and executing query")
            
            data = self.data_agent.get_data(question, steps)
            logger.info(f"Data Agent retrieved {len(data)} records")
            result["agent_logs"].append(f"Data Agent: Retrieved {len(data)} records from database")
            
            if not data:
                logger.warning("No data retrieved from database")
                result["answer"] = "I'm sorry, but I couldn't find any data to answer your question."
                result["insights"] = ["No data available for analysis"]
                result["agent_logs"].append("Pipeline: No data available - terminating early")
                return result
            
            # Step 3: Analysis Agent - Analyze data using pandas
            logger.info("=== STEP 3: ANALYSIS AGENT ===")
            result["agent_logs"].append("Analysis Agent: Using pandas to detect patterns and generate insights")
            
            analysis_result = self.analysis_agent.analyze_data(data, question, steps)
            logger.info(f"Analysis Agent generated {len(analysis_result.get('insights', []))} insights")
            result["agent_logs"].append(f"Analysis Agent: Generated {len(analysis_result.get('insights', []))} insights")
            
            # Step 4: Report Agent - Convert to human-readable answer
            logger.info("=== STEP 4: REPORT AGENT ===")
            result["agent_logs"].append("Report Agent: Converting insights into human-readable answer")
            
            final_report = self.report_agent.generate_report(analysis_result)
            logger.info("Report Agent: Generated human-readable response")
            result["agent_logs"].append("Report Agent: Final report generated successfully")
            
            # Step 5: Aggregate Dashboard Data
            logger.info("=== STEP 5: DASHBOARD DATA AGGREGATION ===")
            result["agent_logs"].append("Analysis Agent: Aggregating dashboard data using pandas")
            
            dashboard_data = self.analysis_agent.aggregate_dashboard_data(data)
            logger.info(f"Dashboard data aggregated: {len(dashboard_data.get('monthlySales', []))} months, {len(dashboard_data.get('regionSales', []))} regions, {len(dashboard_data.get('productSales', []))} products")
            result["agent_logs"].append(f"Dashboard Data: Generated {len(dashboard_data)} data categories")
            
            # Step 6: Detect and Store Insights
            logger.info("=== STEP 6: INSIGHTS DETECTION ===")
            result["agent_logs"].append("Analysis Agent: Detecting insights for database storage")
            
            df = pd.DataFrame(data)
            detected_insights = self.analysis_agent.detect_and_store_insights(df)
            logger.info(f"Detected {len(detected_insights)} insights for storage")
            result["agent_logs"].append(f"Insights Detection: Found {len(detected_insights)} insights")
            
            # Step 7: Store Insights in Database
            logger.info("=== STEP 7: INSIGHTS STORAGE ===")
            result["agent_logs"].append("Data Agent: Storing insights in MySQL database")
            
            if detected_insights:
                try:
                    # Use data agent to store insights
                    self._store_insights_in_database(detected_insights)
                    logger.info(f"Successfully stored {len(detected_insights)} insights in database")
                    result["agent_logs"].append(f"Insights Storage: Stored {len(detected_insights)} insights")
                except Exception as e:
                    logger.error(f"Failed to store insights: {e}")
                    result["agent_logs"].append(f"Insights Storage Error: {str(e)}")
            
            # Assemble final result
            result["answer"] = final_report.get("answer", "No answer generated")
            result["insights"] = final_report.get("insights", [])
            result["chartData"] = dashboard_data
            
            # Add context if available
            if "context" in final_report:
                result["context"] = final_report["context"]
            
            # Add detected insights
            if detected_insights:
                result["detected_insights"] = detected_insights
            
            logger.info("=== PIPELINE COMPLETED SUCCESSFULLY ===")
            logger.info(f"Final answer: {result['answer']}")
            logger.info(f"Total insights: {len(result['insights'])}")
            
            return result
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            result["agent_logs"].append(f"Pipeline Error: {str(e)}")
            result["answer"] = "I'm sorry, but I encountered an error while processing your question."
            result["insights"] = [f"Error: {str(e)}"]
            return result
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get status of all agents in the pipeline
        """
        return {
            "pipeline_status": "active",
            "agents": {
                "planner": "ready",
                "data": "ready", 
                "analysis": "ready",
                "report": "ready"
            },
            "flow": ["Planner → Data → Analysis → Report"]
        }
    
    def _store_insights_in_database(self, insights: List[Dict[str, Any]]):
        """
        Store detected insights in MySQL database
        """
        try:
            # Use data agent to execute insert queries
            data_agent = DataAgent()
            
            for insight in insights:
                insert_query = """
                    INSERT INTO insights (type, message, value, category, created_at) 
                    VALUES (%s, %s, %s, %s, NOW())
                """
                params = (
                    insight.get('type', 'unknown'),
                    insight.get('message', ''),
                    insight.get('value', 0),
                    insight.get('category', 'general')
                )
                
                data_agent.execute_insert_query(insert_query, params)
                logger.debug(f"Stored insight: {insight.get('type')}")
            
            logger.info(f"Successfully stored {len(insights)} insights in database")
            
        except Exception as e:
            logger.error(f"Failed to store insights in database: {e}")
            raise Exception(f"Database storage failed: {e}")
    
    def log_execution_order(self):
        """
        Log the agent execution order for debugging
        """
        logger.info("AGENT EXECUTION ORDER:")
        logger.info("1. Planner Agent - Plans query and generates steps")
        logger.info("2. Data Agent - Converts NL to SQL and fetches data")
        logger.info("3. Analysis Agent - Uses pandas to analyze data")
        logger.info("4. Report Agent - Formats insights into human-readable answer")
        logger.info("5. Pipeline - Returns final consolidated result")

# Initialize global pipeline instance
agent_pipeline = AgentPipeline()
