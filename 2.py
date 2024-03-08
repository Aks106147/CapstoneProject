from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Define your database connection details
db_config = {
    'user': 'app',
    'password': 'appuser',
    'host': '127.0.0.1',
    'database': 'historicaldata',
}

# Function to create a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Route to get historical data for a specific ticker symbol and date range with specified timestamp interval
@app.route('/historical_data')
def get_historical_data():
    # Get the query parameters from the request
    ticker = request.args.get('ticker')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    timestamp_interval = int(request.args.get('timestamp_interval', default=1))

    # Check if the ticker symbol, date range, and timestamp interval are provided
    if not ticker:
        return jsonify({'error': 'Ticker symbol is missing in the request parameters'}), 400
    if not start_date or not end_date:
        return jsonify({'error': 'Start date or end date is missing in the request parameters'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch historical data for the specified ticker symbol, date range, and timestamp interval
    query = """
        SELECT * 
        FROM historical_data 
        WHERE ticker = %s 
        AND timestamp BETWEEN %s AND %s 
        AND MOD(MINUTE(timestamp), %s) = 0
    """
    cursor.execute(query, (ticker, start_date, end_date, timestamp_interval))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
