import requests
import json

def test_api_fix():
    """Test the API to verify the business response generator is working"""
    
    # Test queries
    test_queries = [
        "total revenue",
        "recent sales", 
        "sales by region"
    ]
    
    for query in test_queries:
        print(f"\n=== Testing Query: '{query}' ===")
        
        try:
            response = requests.post(
                "http://localhost:8000/ai/query",
                json={"question": query},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                data = result.get("data", {})
                
                answer = data.get("answer", "No answer")
                insights = data.get("insights", [])
                
                print(f"✅ Status: {result.get('status')}")
                print(f"📝 Answer: {answer}")
                print(f"💡 Insights ({len(insights)}):")
                for i, insight in enumerate(insights, 1):
                    print(f"   {i}. {insight}")
                
                # Check if the old generic response is gone
                if "Analysis completed" in answer:
                    print("❌ BUG STILL EXISTS: Old generic response found")
                else:
                    print("✅ BUG FIXED: No generic response detected")
                
                # Check if insights contain actual data
                has_numbers = any(any(char.isdigit() for char in str(insight)) for insight in insights)
                if has_numbers:
                    print("✅ Insights contain actual data")
                else:
                    print("❌ Insights are generic")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: FastAPI service not running")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_fix()
