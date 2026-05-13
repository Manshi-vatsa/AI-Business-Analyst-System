import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-python-service', 'ai-python-service'))

from services.intelligent_analysis import IntelligentAnalysis

def test_response_improvements():
    """Test the improved response generation logic"""
    
    analyzer = IntelligentAnalysis()
    
    # Test case 1: Single value (total revenue)
    print("=== Test Case 1: Single Value (Total Revenue) ===")
    single_data = [{"total_sales": 60000.00}]
    result1 = analyzer.analyze_data_intelligently(single_data, "total revenue")
    print(f"Answer: {result1['answer']}")
    print(f"Insights: {result1['insights']}")
    print()
    
    # Test case 2: Multiple rows (recent sales)
    print("=== Test Case 2: Multiple Rows (Recent Sales) ===")
    multi_data = [
        {"id": 1, "revenue": 500.00, "product": "Laptop", "date": "2023-01-01"},
        {"id": 2, "revenue": 5200.00, "product": "Phone", "date": "2023-01-02"},
        {"id": 3, "revenue": 2300.00, "product": "Tablet", "date": "2023-01-03"},
        {"id": 4, "revenue": 800.00, "product": "Laptop", "date": "2023-01-04"}
    ]
    result2 = analyzer.analyze_data_intelligently(multi_data, "recent sales")
    print(f"Answer: {result2['answer']}")
    print(f"Insights: {result2['insights']}")
    print()
    
    # Test case 3: Regional analysis
    print("=== Test Case 3: Regional Analysis ===")
    region_data = [
        {"region": "North", "total_revenue": 21500.00, "transactions": 5},
        {"region": "South", "total_revenue": 7500.00, "transactions": 3},
        {"region": "East", "total_revenue": 18000.00, "transactions": 4},
        {"region": "West", "total_revenue": 12000.00, "transactions": 4}
    ]
    result3 = analyzer.analyze_data_intelligently(region_data, "sales by region")
    print(f"Answer: {result3['answer']}")
    print(f"Insights: {result3['insights']}")
    print()
    
    # Test case 4: No data
    print("=== Test Case 4: No Data ===")
    result4 = analyzer.analyze_data_intelligently([], "test query")
    print(f"Answer: {result4['answer']}")
    print(f"Insights: {result4['insights']}")
    print()
    
    # Verify requirements
    print("=== Requirements Verification ===")
    
    # Check answer length (2-4 lines)
    for i, (name, result) in enumerate([
        ("Single Value", result1), 
        ("Multi Row", result2), 
        ("Regional", result3)
    ], 1):
        answer_lines = result['answer'].split('\n')
        print(f"{name}: Answer has {len(answer_lines)} lines - {'✅ PASS' if 2 <= len(answer_lines) <= 4 else '❌ FAIL'}")
    
    # Check if insights are specific and data-driven
    for i, (name, result) in enumerate([
        ("Single Value", result1), 
        ("Multi Row", result2), 
        ("Regional", result3)
    ], 1):
        insights = result['insights']
        has_numbers = any(any(char.isdigit() for char in insight) for insight in insights)
        print(f"{name}: Insights contain numbers - {'✅ PASS' if has_numbers else '❌ FAIL'}")
    
    # Check if no generic phrases
    generic_phrases = ["analysis complete", "analysis completed", "no data available", "no insights available"]
    for i, (name, result) in enumerate([
        ("Single Value", result1), 
        ("Multi Row", result2), 
        ("Regional", result3)
    ], 1):
        answer_lower = result['answer'].lower()
        has_generic = any(phrase in answer_lower for phrase in generic_phrases)
        print(f"{name}: No generic phrases - {'✅ PASS' if not has_generic else '❌ FAIL'}")

if __name__ == "__main__":
    test_response_improvements()
