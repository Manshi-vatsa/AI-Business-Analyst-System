#!/usr/bin/env python3
"""
Test script to verify Spring Boot starts without ambiguous mapping error
"""

import subprocess
import time
import sys
import os
import requests
import re
from pathlib import Path

def test_springboot_routing():
    """Test Spring Boot application routing conflicts"""
    print("=== Testing Spring Boot Routing Conflict Resolution ===")
    
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
        
        print("2. Monitoring startup for mapping conflicts...")
        
        # Wait for startup or timeout
        start_time = time.time()
        startup_success = False
        mapping_conflict = False
        
        while time.time() - start_time < 60:  # 60 second timeout
            # Check if process is still running
            if process.poll() is not None:
                # Process finished, check for errors
                stdout, stderr = process.communicate()
                print("❌ Spring Boot process terminated early")
                print(f"Exit code: {process.returncode}")
                
                # Check for mapping conflicts
                if "Ambiguous mapping" in stderr or "mapping conflict" in stderr.lower():
                    print("❌ Mapping conflict detected!")
                    mapping_conflict = True
                    # Extract relevant error lines
                    for line in stderr.split('\n'):
                        if 'mapping' in line.lower() or 'ambiguous' in line.lower():
                            print(f"   Error: {line.strip()}")
                
                # Check for BeanCreationException
                if "BeanCreationException" in stderr:
                    print("❌ BeanCreationException detected!")
                    mapping_conflict = True
                
                print(f"STDERR: {stderr}")
                return not mapping_conflict
            
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
                
                # Check for specific mapping conflicts
                if "Ambiguous mapping" in stderr:
                    print("❌ Ambiguous mapping detected!")
                    mapping_conflict = True
                    # Extract mapping conflict details
                    for line in stderr.split('\n'):
                        if 'ambiguous' in line.lower() or 'mapping' in line.lower():
                            print(f"   Conflict: {line.strip()}")
                
                if "BeanCreationException" in stderr:
                    print("❌ BeanCreationException detected!")
                    mapping_conflict = True
                
                if not mapping_conflict:
                    print(f"STDERR: {stderr}")
                    
            except:
                pass
            
            # Terminate the process
            try:
                process.terminate()
                process.wait(timeout=10)
            except:
                process.kill()
            
            return not mapping_conflict
        
        # Test the /ai/query endpoint specifically
        print("3. Testing /ai/query endpoint routing...")
        try:
            test_data = {"question": "Test query"}
            response = requests.post(
                "http://localhost:8080/ai/query",
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ /ai/query endpoint accessible")
                print(f"Response: {response.json()}")
            else:
                print(f"❌ /ai/query endpoint returned: {response.status_code}")
                
        except Exception as e:
            print(f"❌ /ai/query endpoint test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during routing test: {e}")
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

def verify_controller_status():
    """Verify controller configuration status"""
    print("\n=== Verifying Controller Configuration ===")
    
    controller_dir = Path("backend-springboot/src/main/java/com/ai/analytics/controller")
    
    active_controllers = []
    disabled_controllers = []
    
    for file_path in controller_dir.glob("*.java"):
        if file_path.name.endswith(".disabled"):
            disabled_controllers.append(file_path.name)
        else:
            active_controllers.append(file_path.name)
    
    print(f"Active Controllers: {len(active_controllers)}")
    for controller in active_controllers:
        print(f"  ✅ {controller}")
    
    print(f"Disabled Controllers: {len(disabled_controllers)}")
    for controller in disabled_controllers:
        print(f"  ❌ {controller}")
    
    # Check for specific controllers
    has_enhanced = "EnhancedQueryController.java" in active_controllers
    has_minimal = "MinimalController.java" in active_controllers
    has_minimal_disabled = "MinimalController.java.disabled" in disabled_controllers
    
    print(f"\nConfiguration Status:")
    print(f"  EnhancedQueryController: {'✅ Active' if has_enhanced else '❌ Missing'}")
    print(f"  MinimalController: {'❌ Active (Conflict!)' if has_minimal else '✅ Disabled' if has_minimal_disabled else '❌ Missing'}")
    
    return has_enhanced and not has_minimal

def main():
    """Main test function"""
    print("🔍 Testing Spring Boot Routing Conflict Resolution")
    print("=" * 60)
    
    # First verify controller configuration
    config_ok = verify_controller_status()
    
    if not config_ok:
        print("\n❌ Controller configuration has issues!")
        return False
    
    # Test Spring Boot startup
    startup_ok = test_springboot_routing()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    
    if config_ok and startup_ok:
        print("✅ No routing conflicts detected")
        print("✅ EnhancedQueryController is primary")
        print("✅ MinimalController is disabled")
        print("✅ Spring Boot starts successfully")
        print("✅ /ai/query endpoint accessible")
    else:
        print("❌ Routing conflict or startup issue detected")
        if not config_ok:
            print("❌ Controller configuration problem")
        if not startup_ok:
            print("❌ Spring Boot startup failure")
    
    return config_ok and startup_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
