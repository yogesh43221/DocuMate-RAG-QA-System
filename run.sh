#!/bin/bash
cd backend && python main.py &
cd frontend && streamlit run app.py
