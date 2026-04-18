#!/bin/bash

echo "Starting Backend..."
cd backend
npm install
npm run build
npm start &
cd ..

echo "Starting Agentic Service..."
cd agentic-service
pip install -r requirements.txt
python main.py &
cd ..

echo "Starting ML APIs..."
cd ml
pip install -r requirements.txt
uvicorn api:app --host 0.0.0.0 --port 8001 &
uvicorn disease_api:app --host 0.0.0.0 --port 5050 &
cd ..

echo "Starting Frontend on port 7860..."
cd frontend
npm install
npm run build
# Vite preview on port 7860 which Hugging Face exposes publicly
npm run preview -- --port 7860 --host 0.0.0.0
