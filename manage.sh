#!/bin/bash
# Requires the database to be up
FLASK_ENV=development DATABASE_URI=postgresql://postgres:usuario@127.0.0.1:5432/mydatabase python manage.py
