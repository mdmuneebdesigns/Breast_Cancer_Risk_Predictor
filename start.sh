#!/bin/bash
# Start FastAPI backend in the background
uvicorn api:app --host 0.0.0.0 --port 8000 &

# Start Flask frontend on port 7860 (Hugging Face default)
# We set FLASK_RUN_PORT=7860 and FLASK_RUN_HOST=0.0.0.0
flask --app app.py run --host=0.0.0.0 --port=7860
