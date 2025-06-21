#!/bin/bash

cd backend

if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment already active."
fi

echo "Starting backend (FastAPI)..."
uvicorn main:app --reload &
BACKEND_PID=$!

cd ../frontend
echo "Starting frontend (Vite)..."
npm run dev &

wait $BACKEND_PID
