import pandas as pd
import ccxt
from datetime import datetime
import mysql.connector

# Define your database connection details
db_config = {

    'user': 'app',
    'password': 'appuser',
    'host': '127.0.0.1',
    'database': 'historicaldata',
} 

# Create a connection to the MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Function to create the historical_data table if it doesn't exist
def create_table():
    create_table_query = """
        CREATE TABLE historical_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ticker VARCHAR(50) NOT NULL,
            timestamp DATETIME NOT NULL,
            open_price DECIMAL(18, 8) NOT NULL,
            close_price DECIMAL(18, 8) NOT NULL,
            high_price DECIMAL(18, 8) NOT NULL,
            low_price DECIMAL(18, 8) NOT NULL,
            volume INT NOT NULL
        );
    """
    cursor.execute(create_table_query)
    conn.commit()

# Function to download and store historical data
def download_and_store_data(symbol, timeframe='1m', limit=60):
    exchange = ccxt.binance()  # You can change this to your preferred exchange
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    for candle in ohlcv:
        timestamp = datetime.utcfromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        values = (symbol, timestamp, candle[1], candle[4], candle[2], candle[3], candle[5])

        insert_query = """
            INSERT INTO historical_data 
            (ticker, timestamp, open_price, close_price, high_price, low_price, volume) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, values)
        conn.commit()

# Main function to download data for Bitcoin and Ethereum
def main():
    #create_table()

    symbols = ['BTC/USDT', 'ETH/USDT']  # You can add more symbols if needed

    for symbol in symbols:
        print(f'Downloading data for {symbol}...')
        download_and_store_data(symbol)

    cursor.close()
    conn.close()

main()