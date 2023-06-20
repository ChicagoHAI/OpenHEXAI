#!/bin/bash
set -Eeuo pipefail

flask --app "openhxai.webapp.app:create_app('config/rcdv/config.yaml')" --debug run