#!/bin/bash
echo "Starting EX3 Demo..."

# Check prerequisites
if ! command -v docker &> /dev/null; then
    echo "Error: docker is not installed."
    exit 1
fi

# Start stack
echo "Bringing up the stack..."
docker compose -f compose.yaml up -d --build

# Wait for health
echo "Waiting for services to be healthy..."
# Basic wait delay
sleep 10
docker compose -f compose.yaml ps

# Display instructions
echo ""
echo "Stack is up!"
echo "Main Backend: http://localhost:8000"
echo "AI Service: http://localhost:8000 (internal port 8000 mapped? No, check compose)"
echo "Frontend: http://localhost:8501"
echo ""
echo "Please open http://localhost:8501 in your browser to test the full flow."
echo "1. Create a creature."
echo "2. See it appear with an AI-generated avatar."
echo ""
read -p "Press Enter to stop the demo..."
docker compose -f compose.yaml down
echo "Demo stopped."
