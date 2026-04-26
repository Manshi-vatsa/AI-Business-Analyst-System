#!/usr/bin/env python3
"""
Fallback Python FastAPI server with port detection
Automatically finds available port if 8000 is blocked
"""

import socket
import sys
import uvicorn
from main import app

def find_available_port(start_port=8000, max_port=8010):
    """Find an available port starting from start_port"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                if result != 0:  # Port is available
                    return port
        except Exception:
            continue
    return None

def main():
    """Start FastAPI server with fallback port detection"""
    
    # Try port 8000 first
    preferred_port = 8000
    available_port = find_available_port(preferred_port)
    
    if available_port is None:
        print("❌ No available ports found in range 8000-8010")
        sys.exit(1)
    
    if available_port != preferred_port:
        print(f"⚠️  Port {preferred_port} is blocked, using port {available_port}")
        print(f"📝 Update Spring Boot to use: http://localhost:{available_port}/ai/query")
    else:
        print(f"✅ Using preferred port {available_port}")
    
    print("=" * 50)
    print("🚀 AI Business Analyst Service Starting")
    print(f"📍 Port: {available_port}")
    print(f"🌐 URL: http://localhost:{available_port}")
    print("=" * 50)
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=available_port,
            reload=False,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
