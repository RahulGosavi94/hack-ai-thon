#!/bin/bash

echo "=========================================="
echo "Airline Disruption Management System"
echo "Startup Script"
echo "=========================================="
echo ""

# Check if Flask is running
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 5000 already in use. Killing existing process..."
    kill -9 $(lsof -t -i :5000) 2>/dev/null
    sleep 1
fi

# Check if test_data files exist
if [ ! -f "test_data/flights_data.json" ]; then
    echo "⚠️  Test data files not found. Generating..."
    python3 data_generator.py
fi

# Start Flask API server in background
echo "🚀 Starting Flask API Server..."
python3 app.py > api.log 2>&1 &
API_PID=$!
echo "✅ Flask API Server started (PID: $API_PID)"
sleep 2

# Check if server is running
if ! lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "❌ Failed to start Flask API Server"
    cat api.log
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ System Started Successfully!"
echo "=========================================="
echo ""
echo "📋 Available URLs:"
echo "  • Web UI: file://$(pwd)/index.html"
echo "  • Or serve locally: python3 -m http.server 8000"
echo "  • Then visit: http://localhost:8000"
echo ""
echo "🔌 API Server: http://localhost:5000"
echo "📚 API Docs: See QUICK_START.md"
echo ""
echo "🤖 Optional: Start Ollama in another terminal"
echo "  • Run: ollama serve"
echo "  • Pull model: ollama pull llama2"
echo ""
echo "To stop the system, run: kill $API_PID"
echo ""
