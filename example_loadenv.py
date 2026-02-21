#!/usr/bin/env python3
# Example: Reading API key from environment variables in Python
# Make sure to install python-dotenv: pip install python-dotenv

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')

if not api_key:
    print('ERROR: API_KEY is not set in environment variables')
    print('Please set your API key in the .env file or system environment')
    print('See README_ENV.md for setup instructions')
    exit(1)

print('✅ Environment variables loaded successfully')
print(f'API Key: {api_key[:8]}...')
print(f'Secret Key: {"Set" if secret_key else "Not set"}')

# Example API call using the key
def make_api_call():
    import requests  # This would need requests library installed
    
    url = 'https://api.example.com/data'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    print(f'Making API call to {url} with API key')
    # Actual API call would go here
    # response = requests.get(url, headers=headers)
    # return response.json()

if __name__ == '__main__':
    make_api_call()