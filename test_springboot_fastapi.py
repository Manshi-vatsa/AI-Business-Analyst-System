#!/usr/bin/env python3
"""
Test script to verify Spring Boot to FastAPI communication
"""

import requests
import json
import time
import sys

def test_fastapi_directly():
    """Test FastAPI service directly"""
    print("=== Testing FastAPI Service Directly ===")
    
    try:
        # Test health endpoint
        health_response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"FastAPI Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"FastAPI Health Response: {health_response.json()}")
        
        # Test query endpoint
        query_data = {"question": "What are the total sales?"}
        query_response = requests.post("http://localhost:8000/ai/query", 
                                     json=query_data, timeout=30)
        print(f"FastAPI Query Status: {query_response.status_code}")
        if query_response.status_code == 200:
            response_data = query_response.json()
            print(f"FastAPI Query Response: {json.dumps(response_data, indent=2)}")
            
            # Check for expected structure
            if response_data.get("status") == "success" and response_data.get("data"):
                data = response_data["data"]
                if "answer" in data and "insights" in data:
                    print("✅ FastAPI response structure is correct")
                    return True
                else:
                    print("❌ FastAPI response structure is incorrect")
                    return False
            else:
                print("❌ FastAPI response missing expected fields")
                return False
        else:
            print(f"❌ FastAPI query failed: {query_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ FastAPI service not reachable at http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing FastAPI: {e}")
        return False

def test_springboot_to_fastapi():
    """Test Spring Boot to FastAPI communication"""
    print("\n=== Testing Spring Boot to FastAPI Communication ===")
    
    try:
        # Test Spring Boot health endpoint
        health_response = requests.get("http://localhost:8080/ai/health", timeout=15)
        print(f"Spring Boot Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"Spring Boot Health Response: {json.dumps(health_data, indent=2)}")
            
            if health_data.get("fastapi_status") == "healthy":
                print("✅ Spring Boot can reach FastAPI")
            else:
                print("❌ Spring Boot cannot reach FastAPI")
                return False
        else:
            print(f"❌ Spring Boot health check failed: {health_response.text}")
            return False
        
        # Test Spring Boot query endpoint
        query_data = {"question": "What are the total sales?"}
        query_response = requests.post("http://localhost:8080/ai/query", 
                                     json=query_data, timeout=45)
        print(f"Spring Boot Query Status: {query_response.status_code}")
        
        if query_response.status_code == 200:
            response_data = query_response.json()
            print(f"Spring Boot Query Response: {json.dumps(response_data, indent=2)}")
            
            # Check for expected structure (should be unwrapped)
            if "answer" in response_data and "insights" in response_data:
                print("✅ Spring Boot response structure is correct")
                if "mock response" not in response_data.get("answer", "").lower():
                    print("✅ Real FastAPI response (not mock)")
                    return True
                else:
                    print("❌ Still getting mock response")
                    return False
            else:
                print("❌ Spring Boot response structure is incorrect")
                return False
        else:
            print(f"❌ Spring Boot query failed: {query_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Spring Boot service not reachable at http://localhost:8080")
        return False
    except Exception as e:
        print(f"❌ Error testing Spring Boot: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 Testing Spring Boot to FastAPI Communication")
    print("=" * 50)
    
    # Test FastAPI directly first
    fastapi_ok = test_fastapi_directly()
    
    if not fastapi_ok:
        print("\n❌ FastAPI service is not working. Please start it first:")
        print("   cd ai-python-service")
        print("   python main.py")
        return
    
    # Wait a moment for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    time.sleep(2)
    
    # Test Spring Boot to FastAPI communication
    springboot_ok = test_springboot_to_fastapi()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"   FastAPI Service: {'✅ Working' if fastapi_ok else '❌ Not Working'}")
    print(f"   Spring Boot → FastAPI: {'✅ Working' if springboot_ok else '❌ Not Working'}")
    
    if fastapi_ok and springboot_ok:
        print("\n🎉 All tests passed! Communication is working correctly.")
        print("   Android app should now receive real responses instead of mock data.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")
        print("   Make sure both services are running:")
        print("   1. FastAPI: python main.py (port 8000)")
        print("   2. Spring Boot: ./mvnw spring-boot:run (port 8080)")

if __name__ == "__main__":
    main()
