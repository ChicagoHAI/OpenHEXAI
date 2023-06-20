#!/bin/bash
set -Eeuo pipefail

ADDR=0.0.0.0
PORT=7777

gunicorn --timeout 120\
	--bind unix:/data/webapps/openhexai1/webapp.sock \
	"openhxai.webapp.app:create_app('config/rcdv/config.yaml')" \
	--error-logfile /data/webapps/openhexai1/logs/gunicorn_error.log \
	--access-logfile /data/webapps/openhexai1/logs/gunicorn_access.log    
