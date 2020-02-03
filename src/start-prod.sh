#!/bin/bash

source ../set_environ
gunicorn app.main:app -w 12 --bind 0.0.0.0:8000 --access-logfile - --error-logfile - -k uvicorn.workers.UvicornWorker
