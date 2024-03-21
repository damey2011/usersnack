#!/bin/sh

set -ex

echo "Prestart checks started.."
python scripts/prestart.py
echo "Prestart checks complete.."

echo "Starting application.."
python -m app
