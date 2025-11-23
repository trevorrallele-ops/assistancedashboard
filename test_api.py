import requests
import json

try:
    response = requests.get('http://localhost:8080/api/stocks', timeout=10)
    print('Status:', response.status_code)
    if response.status_code == 200:
        data = response.json()
        print('Stock data retrieved successfully!')
        for symbol, info in data.items():
            print(f'{symbol}: ${info.get("price", "N/A")} ({info.get("change", 0):.2f}%)')
    else:
        print('Response:', response.text)
except Exception as e:
    print('Error:', e)