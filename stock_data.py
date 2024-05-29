import requests
import json
api_key = '94XIQWNOKQALSWZI'
def fetch_stock_data(symbol) :
    url = (f"https://www.alphavantage.co/query")
    params = {
        'function' : "TIME_SERIES_INTRADAY",
        'symbol' : symbol,
        'apikey' : api_key,
        'interval' : '5min'
    }
    response = requests.get(url,params=params)
    #print(response)
    if (response.status_code == 200) :
        data = response.json()
        formatted_data = json.dumps(data,indent=4)
        print(f'Stock Symbol {stock_symbol} and data {formatted_data}')
        
    
   



stock_symbol = ['AAPL','MSFT','GOOGL']
stock_data = fetch_stock_data(stock_symbol)
