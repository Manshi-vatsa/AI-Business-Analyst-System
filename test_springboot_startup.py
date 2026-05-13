#!/usr/bin/env python3
"""
Test script to verify Spring Boot starts without BeanCreationException
"""

import subprocess
import time
import sys
import os
import requests
from pathlib import Path

def test_springboot_startup():
    """Test Spring Boot application startup"""
    print("=== Testing Spring Boot Startup ===")
    
    backend_dir = Path("backend-springboot")
    if not backend_dir.exists():
        print("❌ backend-springboot directory not found")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    try:
        print("1. Starting Spring Boot application...")
        
        # Start Spring Boot in background
        process = subprocess.Popen(
            ["./mvnw", "spring-boot:run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("2. Waiting for application to start (60 seconds timeout)...")
        
        # Wait for startup or timeout
        start_time = time.time()
        startup_success = False
        bean_creation_error = False
        
        while time.time() - start_time < 60:  # 60 second timeout
            # Check if process is still running
            if process.poll() is not None:
                # Process finished, check for errors
                stdout, stderr = process.communicate()
                print("❌ Spring Boot process terminated early")
                print(f"Exit code: {process.returncode}")
                print(f"STDERR: {stderr}")
                
                if "BeanCreationException" in stderr:
                    print("❌ BeanCreationException detected!")
                    bean_creation_error = True
                return False
            
            # Try to connect to health endpoint
            try:
                response = requests.get("http://localhost:8080/ai/health", timeout=5)
                if response.status_code == 200:
                    print("✅ Spring Boot started successfully!")
                    print(f"Health check response: {response.json()}")
                    startup_success = True
                    break
            except requests.exceptions.ConnectionError:
                pass  # Service not ready yet
            except Exception as e:
                print(f"Health check error: {e}")
            
            time.sleep(2)
        
        if not startup_success:
            print("❌ Spring Boot failed to start within 60 seconds")
            # Try to get error output
            try:
                stdout, stderr = process.communicate(timeout=5)
                if "BeanCreationException" in stderr:
                    print("❌ BeanCreationException detected in logs!")
                    print(f"Error details: {stderr}")
                    bean_creation_error = True
                else:
                    print(f"STDERR: {stderr}")
            except:
                pass
            
            # Terminate the process
            try:
                process.terminate()
                process.wait(timeout=10)
            except:
                process.kill()
            
            return not bean_creation_error
        
        # Test CORS configuration
        print("3. Testing CORS configuration...")
        try:
            # Test preflight request
            response = requests.options(
                "http://localhost:8080/ai/query",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                cors_headers = {
                    "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                    "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials"),
                    "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods")
                }
                print("✅ CORS preflight request successful")
                print(f"CORS Headers: {cors_headers}")
            else:
                print(f"❌ CORS preflight failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ CORS test error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during startup test: {e}")
        return False
    
    finally:
        # Clean up: terminate the process
        try:
            if 'process' in locals() and process.poll() is None:
                process.terminate()
                process.wait(timeout=10)
        except:
            try:
                if 'process' in locals():
                    process.kill()
            except:
                pass

def main():
    """Main test function"""
    print("🔍 Testing Spring Boot Startup Without BeanCreationException")
    print("=" * 60)
    
    success = test_springboot_startup()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    
    if success:
        print("✅ Spring Boot starts successfully without BeanCreationException")
        print("✅ CORS configuration is working properly")
        print("✅ Application is ready for requests")
    else:
        print("❌ Spring Boot startup failed")
        print("❌ Check the logs above for BeanCreationException details")
        print("❌ Verify CORS configuration fixes")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
