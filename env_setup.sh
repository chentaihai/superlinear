#!/bin/bash
# Setup script for environment variables
# Usage: source setup.sh

echo "Setting up environment variables for API client"

# Check if .env file exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    export $(grep -v '^#' .env | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "⚠️  No .env file found. Creating .env.example as template."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Created .env from example. Please edit with your actual keys."
    else
        echo "ERROR: .env.example not found. Cannot create .env file."
    fi
fi

# Verify GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY is not set. Please add it to .env file or export manually."
else
    echo "✅ GEMINI_API_KEY is set (first 8 chars: ${GEMINI_API_KEY:0:8}...)"
fi