from flask import Flask, render_template, jsonify, request
import yfinance as yf
import json
import os
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)
DATA_FILE = 'stock_data.json'

MARKETS = {
    'stocks': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
    'crypto': ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD'],
    'forex': ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X'],
    'commodities': ['GC=F', 'CL=F', 'SI=F', 'NG=F']
}

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
        # Mock data for demo
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

def load_stock_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return fetch_stock_data()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stocks')
def get_stocks():
    return jsonify(load_stock_data())

@app.route('/api/refresh')
def refresh_data():
    return jsonify(fetch_stock_data())

@app.route('/api/historical')
def get_historical():
    symbols_param = request.args.get('symbols')
    market = request.args.get('market', 'stocks')
    start_date = request.args.get('start', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end', datetime.now().strftime('%Y-%m-%d'))
    interval = request.args.get('interval', '1d')
    
    if symbols_param:
        symbols = symbols_param.split(',')
    else:
        symbols = MARKETS.get(market, MARKETS['stocks'])
    data = {}
    
    try:
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date, interval=interval)
                if not hist.empty:
                    data[symbol] = {
                        'dates': hist.index.strftime('%Y-%m-%d').tolist(),
                        'open': hist['Open'].tolist(),
                        'high': hist['High'].tolist(),
                        'low': hist['Low'].tolist(),
                        'close': hist['Close'].tolist(),
                        'volume': hist['Volume'].tolist()
                    }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(data)

@app.route('/api/markets')
def get_markets():
    return jsonify(list(MARKETS.keys()))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)