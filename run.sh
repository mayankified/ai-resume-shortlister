#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🚀 Starting AI Resume Shortlisting App..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ venv not found. Please create virtual environment first."
    exit 1
fi

# Run Streamlit app
streamlit run app.py
