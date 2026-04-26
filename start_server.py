#!/usr/bin/env python3
"""
Production-ready FastAPI startup script
"""

import os
import sys
import uvicorn
from main import app

def main():
    """Main function to start the FastAPI server"""
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    workers = int(os.getenv("WORKERS", 1))
    
    print("=" * 50)
    print("🚀 AI Business Analyst Service Starting")
    print("=" * 50)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Reload: {reload}")
    print(f"Workers: {workers}")
    print("=" * 50)
    
    # Start server
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload,
            workers=workers if not reload else 1,  # Single worker for reload mode
            log_level="info",
            access_log=True,
            use_colors=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
