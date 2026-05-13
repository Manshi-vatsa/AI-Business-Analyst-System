from services.intelligent_analysis import IntelligentAnalysis

def test_improved_responses():
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
        {"id": 3, "revenue": 2300.00, "product": "Tablet", "date": "2023-01-03"}
    ]
    result2 = analyzer.analyze_data_intelligently(multi_data, "recent sales")
    print(f"Answer: {result2['answer']}")
    print(f"Insights: {result2['insights']}")
    print()
    
    # Test case 3: Regional analysis
    print("=== Test Case 3: Regional Analysis ===")
    region_data = [
        {"region": "North", "total_revenue": 21500.00, "transactions": 5},
        {"region": "South", "total_revenue": 7500.00, "transactions": 3}
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
    for name, result in [("Single Value", result1), ("Multi Row", result2), ("Regional", result3)]:
        answer_lines = result['answer'].split('\n')
        line_count = len(answer_lines)
        status = "✅ PASS" if 2 <= line_count <= 4 else "❌ FAIL"
        print(f"{name}: Answer has {line_count} lines - {status}")
    
    # Check if insights are specific and data-driven
    for name, result in [("Single Value", result1), ("Multi Row", result2), ("Regional", result3)]:
        insights = result['insights']
        has_numbers = any(any(char.isdigit() for char in insight) for insight in insights)
        status = "✅ PASS" if has_numbers else "❌ FAIL"
        print(f"{name}: Insights contain numbers - {status}")
    
    # Check if no generic phrases
    generic_phrases = ["analysis complete", "analysis completed", "no data available", "no insights available"]
    for name, result in [("Single Value", result1), ("Multi Row", result2), ("Regional", result3)]:
        answer_lower = result['answer'].lower()
        has_generic = any(phrase in answer_lower for phrase in generic_phrases)
        status = "✅ PASS" if not has_generic else "❌ FAIL"
        print(f"{name}: No generic phrases - {status}")

if __name__ == "__main__":
    test_improved_responses()
