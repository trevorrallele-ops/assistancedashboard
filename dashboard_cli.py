import json
import os
import time
from datetime import datetime
import yfinance as yf
import sys

DATA_FILE = 'stock_data.json'

def fetch_stock_data():
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    data = {}
    
    try:
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            data[symbol] = {
                'price': info.get('currentPrice', 0),
                'change': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'updated': datetime.now().isoformat()
            }
    except Exception as e:
        print(f"YFinance error: {e}. Using mock data.")
        import random
        data = {
            'AAPL': {'price': 175.43, 'change': random.uniform(-3, 3), 'volume': 45234567, 'updated': datetime.now().isoformat()},
            'GOOGL': {'price': 2847.32, 'change': random.uniform(-3, 3), 'volume': 23456789, 'updated': datetime.now().isoformat()},
            'MSFT': {'price': 378.85, 'change': random.uniform(-3, 3), 'volume': 34567890, 'updated': datetime.now().isoformat()},
            'TSLA': {'price': 248.42, 'change': random.uniform(-3, 3), 'volume': 56789012, 'updated': datetime.now().isoformat()}
        }
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)
    
    return data

def display_dashboard():
    while True:
        print('\n' * 50)
        
        stocks = fetch_stock_data()
        
        print("\n" + "="*70)
        print(" "*20 + "📊 STOCK DASHBOARD 📊")
        print("="*70 + "\n")
        
        for symbol, data in stocks.items():
            price = data['price']
            change = data['change']
            volume = data['volume']
            
            arrow = "📈" if change >= 0 else "📉"
            color_code = "\033[92m" if change >= 0 else "\033[91m"
            reset_code = "\033[0m"
            
            print(f"{symbol:6} | ${price:>10.2f} | {color_code}{arrow} {change:>7.2f}%{reset_code} | Vol: {volume:>12,}")
        
        print("\n" + "="*70)
        print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Press Ctrl+C to exit, refreshing every 60 seconds...")
        print("="*70 + "\n")
        
        time.sleep(60)

if __name__ == '__main__':
    try:
        display_dashboard()
    except KeyboardInterrupt:
        print("\n\nDashboard closed.")
        sys.exit(0)