#!/usr/bin/env python3
"""
Test script for LLM-based SQL generation
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_llm_service():
    """Test LLM service SQL generation"""
    try:
        # Import LLM service
        from services.llm_service import llm_service
        
        logger.info("=== Testing LLM Service SQL Generation ===")
        
        # Test questions
        test_questions = [
            "What are the total sales?",
            "Show me sales by region",
            "What's the average revenue per product?",
            "Which product has the highest revenue?",
            "Show me monthly sales trends"
        ]
        
        test_steps = [
            ["analyze_question", "fetch_data", "generate_insights"],
            ["regional_analysis", "aggregate_data"],
            ["product_analysis", "calculate_averages"],
            ["top_performer", "rank_products"],
            ["time_series", "monthly_aggregation"]
        ]
        
        for i, question in enumerate(test_questions):
            logger.info(f"\n--- Test {i+1}: {question} ---")
            
            try:
                # Generate SQL
                sql = llm_service.generate_sql(question, test_steps[i])
                logger.info(f"✅ Generated SQL: {sql}")
                
                # Validate SQL
                is_valid = llm_service.validate_sql(sql)
                logger.info(f"✅ SQL Validation: {'PASS' if is_valid else 'FAIL'}")
                
                # Generate explanation
                explanation = llm_service.explain_sql(sql)
                logger.info(f"✅ Explanation: {explanation}")
                
            except Exception as e:
                logger.error(f"❌ Error in test {i+1}: {e}")
        
        logger.info("\n=== LLM Service Test Complete ===")
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.info("Make sure OpenAI API key is set in environment variables")
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")

def test_data_agent_integration():
    """Test DataAgent with LLM integration"""
    try:
        from agents.data_agent import DataAgent
        
        logger.info("\n=== Testing DataAgent LLM Integration ===")
        
        # Initialize DataAgent
        data_agent = DataAgent()
        logger.info("✅ DataAgent initialized")
        
        # Test SQL generation
        test_question = "What are the total sales?"
        test_steps = ["analyze_question", "fetch_data", "generate_insights"]
        
        sql = data_agent.natural_language_to_sql(test_question, test_steps)
        logger.info(f"✅ Generated SQL: {sql}")
        
        logger.info("\n=== DataAgent Integration Test Complete ===")
        
    except Exception as e:
        logger.error(f"❌ DataAgent test error: {e}")

def main():
    """Main test function"""
    logger.info("Starting LLM SQL Generation Tests...")
    
    # Check environment
    if not os.getenv('OPENAI_API_KEY'):
        logger.warning("⚠️  OPENAI_API_KEY not set in environment variables")
        logger.info("Set OPENAI_API_KEY to test with real OpenAI API")
        logger.info("Tests will use fallback behavior")
    
    # Run tests
    test_llm_service()
    test_data_agent_integration()
    
    logger.info("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
