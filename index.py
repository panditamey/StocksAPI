from flask import Flask, jsonify, request, Response
import yfinance as yf

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to Stock API'}), 200

@app.route('/api/getDetails', methods=['GET'])
def get_details():
    symbol = request.args.get('symbol')
    exchange = ".NS" if request.args.get('exchange')=="NSE" else ".BO"
    time_period = request.args.get('time', 'max')
    json = request.args.get('json', "false")
    start = request.args.get('start', None)
    end = request.args.get('end', None)


    if symbol is None:
        return jsonify({'error': 'Symbol parameter is missing'}), 400

    try:
        stock = yf.Ticker(symbol+exchange)
        if(start):
            if(end):
                data = stock.history(start=start, end=end)
            else:
                data = stock.history(start=start)
        else:
            data = stock.history(period=time_period)
        if(json=="true"):
            return data.to_json(orient='index'), 200
        
        # Convert DataFrame to CSV
        csv_data = data.to_csv(index_label='Date', float_format='%.2f')

        # Create response with CSV data
        response = Response(csv_data, mimetype='text/csv')
        response.headers["Content-Disposition"] = "attachment; filename=stock_data.csv"
        
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
