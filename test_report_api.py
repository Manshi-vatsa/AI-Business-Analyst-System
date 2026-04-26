#!/usr/bin/env python3
"""
Test script for the report generation API
"""

import requests
import json
import base64
import os
from datetime import datetime

def test_report_api():
    """Test the report generation API endpoint"""
    
    # API configuration
    base_url = "http://localhost:8000"
    endpoint = "/ai/report"
    
    # Test data
    report_request = {
        "report_type": "pdf"
    }
    
    print(f"Testing report generation API...")
    print(f"URL: {base_url}{endpoint}")
    print(f"Request: {json.dumps(report_request, indent=2)}")
    
    try:
        # Make the API call
        response = requests.post(
            f"{base_url}{endpoint}",
            json=report_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Check if report was generated successfully
            if result.get("status") == "success":
                print(f"\nReport generated successfully!")
                print(f"Report Type: {result.get('report_type')}")
                print(f"Filename: {result.get('filename')}")
                print(f"Content Type: {result.get('content_type')}")
                
                # Save the report to file (optional)
                if result.get("data"):
                    try:
                        # Decode base64 data
                        pdf_data = base64.b64decode(result["data"])
                        
                        # Save to file
                        filename = result.get("filename", f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                        with open(filename, "wb") as f:
                            f.write(pdf_data)
                        
                        print(f"Report saved as: {filename}")
                        print(f"File size: {len(pdf_data)} bytes")
                        
                    except Exception as e:
                        print(f"Error saving report: {e}")
                
                # Display insights
                if result.get("insights"):
                    print(f"\nInsights included in report:")
                    insights = result["insights"]
                    if isinstance(insights, dict):
                        for key, value in insights.items():
                            print(f"  {key}: {value}")
                    else:
                        print(f"  {insights}")
            else:
                print(f"Report generation failed: {result.get('error', 'Unknown error')}")
        
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server")
        print("Make sure the Python service is running on http://localhost:8000")
        
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        
    except Exception as e:
        print(f"Error: {e}")

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("Health check passed: Service is running")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except:
        print("Health check failed: Service not reachable")
        return False

if __name__ == "__main__":
    print("=== Report API Test ===\n")
    
    # First check if service is running
    if test_health_check():
        print("\n" + "="*50)
        test_report_api()
    else:
        print("\nPlease start the Python AI service first:")
        print("cd ai-python-service")
        print("python main.py")
    
    print("\n=== Test Complete ===")
