import os
import sys
import subprocess
import time
import threading
import streamlit as st

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def run_backend():
    """Run FastAPI backend in background"""
    import uvicorn
    from backend.main import app
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

# Start backend in daemon thread
if 'backend_started' not in st.session_state:
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    time.sleep(2)  # Wait for backend to start
    st.session_state.backend_started = True

# Now run the frontend
exec(open(os.path.join('frontend', 'app.py')).read())
