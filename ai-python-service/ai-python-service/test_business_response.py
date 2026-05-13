from services.business_response_generator import generate_business_response

def test_business_response():
    """Test the new business response generation logic"""
    
    # Test case 1: No data
    print("=== Test Case 1: No Data ===")
    result1 = generate_business_response([])
    print(f"Answer: {result1['answer']}")
    print(f"Insights: {result1['insights']}")
    print()
    
    # Test case 2: Single value (total revenue)
    print("=== Test Case 2: Single Value (Total Revenue) ===")
    single_data = [{"total_sales": 60000}]
    result2 = generate_business_response(single_data)
    print(f"Answer: {result2['answer']}")
    print(f"Insights: {result2['insights']}")
    print()
    
    # Test case 3: Multiple rows with revenue and product
    print("=== Test Case 3: Multiple Rows (Sales Data) ===")
    multi_data = [
        {"revenue": 5200, "product": "Laptop", "region": "North"},
        {"revenue": 800, "product": "Phone", "region": "South"},
        {"revenue": 2300, "product": "Tablet", "region": "North"},
        {"revenue": 1500, "product": "Laptop", "region": "East"}
    ]
    result3 = generate_business_response(multi_data)
    print(f"Answer: {result3['answer']}")
    print(f"Insights: {result3['insights']}")
    print()
    
    # Test case 4: Regional data
    print("=== Test Case 4: Regional Analysis ===")
    region_data = [
        {"region": "North", "total_revenue": 21500, "transactions": 5},
        {"region": "South", "total_revenue": 7500, "transactions": 3},
        {"region": "East", "total_revenue": 18000, "transactions": 4}
    ]
    result4 = generate_business_response(region_data)
    print(f"Answer: {result4['answer']}")
    print(f"Insights: {result4['insights']}")
    print()
    
    # Verify requirements
    print("=== Requirements Verification ===")
    
    # Check answer length (2-4 lines)
    for i, (name, result) in enumerate([
        ("Single Value", result2), 
        ("Multi Row", result3), 
        ("Regional", result4)
    ], 1):
        answer_lines = result['answer'].split('. ')
        line_count = len([line for line in answer_lines if line.strip()])
        print(f"{name}: Answer has {line_count} parts - {'✅ PASS' if 2 <= line_count <= 4 else '❌ FAIL'}")
    
    # Check if insights are specific and data-driven
    for i, (name, result) in enumerate([
        ("Single Value", result2), 
        ("Multi Row", result3), 
        ("Regional", result4)
    ], 1):
        insights = result['insights']
        has_numbers = any(any(char.isdigit() for char in insight) for insight in insights)
        print(f"{name}: Insights contain numbers - {'✅ PASS' if has_numbers else '❌ FAIL'}")
    
    # Check if no generic phrases
    generic_phrases = ["analysis complete", "analysis completed", "no data available", "no insights available"]
    for i, (name, result) in enumerate([
        ("Single Value", result2), 
        ("Multi Row", result3), 
        ("Regional", result4)
    ], 1):
        answer_lower = result['answer'].lower()
        has_generic = any(phrase in answer_lower for phrase in generic_phrases)
        print(f"{name}: No generic phrases - {'✅ PASS' if not has_generic else '❌ FAIL'}")
    
    # Check if insights are limited to 3
    for i, (name, result) in enumerate([
        ("Single Value", result2), 
        ("Multi Row", result3), 
        ("Regional", result4)
    ], 1):
        insights_count = len(result['insights'])
        print(f"{name}: Insights limited to 3 - {'✅ PASS' if insights_count <= 3 else '❌ FAIL'}")

if __name__ == "__main__":
    test_business_response()
