#!/bin/sh

set -ex

echo "Prestart checks started.."
python scripts/prestart.py
echo "Prestart checks complete.."

echo "Starting application.."
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
