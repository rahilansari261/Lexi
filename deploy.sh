#!/bin/bash

# Jagriti Case Search API Deployment Script

echo "🚀 Deploying Jagriti Case Search API..."

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages

# Make scripts executable
chmod +x test_api.py
chmod +x deploy.sh

# Start the Flask application
echo "🌐 Starting Flask application..."
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the enhanced Flask app
python3 enhanced_flask_app.py