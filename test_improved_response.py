import requests
import json

def test_improved_response():
    """Test the improved response generation"""
    
    # Test queries
    test_queries = [
        "recent sales",
        "total revenue",
        "top product",
        "sales by region"
    ]
    
    for query in test_queries:
        print(f"\n=== Testing Query: '{query}' ===")
        
        try:
            response = requests.post(
                "http://localhost:8000/ai/query",
                json={"question": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                data = result.get("data", {})
                
                print(f"✅ Status: {result.get('status')}")
                print(f"📝 Answer: {data.get('answer', 'No answer')}")
                print(f"💡 Insights: {len(data.get('insights', []))} found")
                
                for i, insight in enumerate(data.get('insights', []), 1):
                    print(f"   {i}. {insight}")
                
                print(f"🔍 SQL Query: {data.get('sql_query', 'No SQL')}")
                print(f"📊 Results: {len(data.get('results', []))} records")
                
                # Check if response format is correct
                required_fields = ['answer', 'insights', 'sql_query', 'results']
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"❌ Missing fields: {missing_fields}")
                else:
                    print("✅ Response format is correct")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_improved_response()
