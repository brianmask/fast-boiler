#! /usr/bin/env bash

# Run migrations
PYTHONPATH=. alembic upgrade head

# Create initial data in DB
PYTHONPATH=. python app/initialize_data.py
