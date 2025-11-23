import sys
import json
import os
from datetime import datetime
import yfinance as yf
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

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

class StockCard(QWidget):
    def __init__(self, symbol, data):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        symbol_label = QLabel(symbol)
        symbol_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        
        price_label = QLabel(f"${data['price']:.2f}")
        price_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        
        change = data['change']
        change_color = QColor(76, 175, 80) if change >= 0 else QColor(244, 67, 54)
        change_label = QLabel(f"{'+' if change >= 0 else ''}{change:.2f}%")
        change_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        change_label.setStyleSheet(f"color: rgb({change_color.red()}, {change_color.green()}, {change_color.blue()})")
        
        volume_label = QLabel(f"Vol: {data['volume']:,}")
        volume_label.setFont(QFont('Arial', 10))
        
        layout.addWidget(symbol_label)
        layout.addWidget(price_label)
        layout.addWidget(change_label)
        layout.addWidget(volume_label)
        
        self.setStyleSheet("background-color: white; border-radius: 8px; padding: 15px; border: 1px solid #ddd;")
        self.setLayout(layout)

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Dashboard')
        self.setGeometry(100, 100, 1000, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        header = QLabel('Stock Dashboard')
        header.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        main_layout.addWidget(header)
        
        self.refresh_btn = QPushButton('Refresh Data')
        self.refresh_btn.clicked.connect(self.refresh_data)
        main_layout.addWidget(self.refresh_btn)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        scroll.setWidget(self.grid_widget)
        
        main_layout.addWidget(scroll)
        central_widget.setLayout(main_layout)
        
        self.load_stocks()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_stocks)
        self.timer.start(60000)
    
    def load_stocks(self):
        stocks = fetch_stock_data()
        
        while self.grid_layout.count():
            self.grid_layout.takeAt(0).widget().deleteLater()
        
        row, col = 0, 0
        for symbol, data in stocks.items():
            card = StockCard(symbol, data)
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
    
    def refresh_data(self):
        self.load_stocks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())