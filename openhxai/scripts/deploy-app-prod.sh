#!/bin/bash
set -Eeuo pipefail

ADDR=0.0.0.0
PORT=7777

python -m gunicorn -w 1 -b $ADDR:$PORT --timeout 120 \
    "openhxai.webapp.app:create_app('config/compas/config.yaml')"
    