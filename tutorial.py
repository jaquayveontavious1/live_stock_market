import yfinance as yf
import sqlite3
import pandas as pd


db = sqlite3.connect("database_db.db")
cursor = db.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS stock_market (
    Symbol TEXT PRIMARY KEY,
    Price REAL,
    Volume INTEGER,
    Change_pct REAL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    '''
)
db.commit()


def fetch_data () :
    symbols = ['AAPL','MSFT','GOOGL','AMZN','NFLX','TSLA','NVDA','ORCL','IBM','INTC','JPM','BAC','C','GS','MS','JNJ','PFE','MRK','ABBV','UNH','KO','PEP','PG','UL','MCD','XOM','CVX','BP','SO','WMT','HD','COST','TGT','BBY','LOW','HD','NEE','DUK','SO','UNP','GE','MMM','CAT','BA','COP',]
    data = yf.download(symbols,period='1d',interval='5m')
    
    stock_data_list = [] 
    for symbol in symbols: #for loop for each symbol in symbols array (iloc[]--> it used in pandas for number indexing)
        latest_data = data['Close'][symbol].iloc[-1] #inside the data we are accessing the column of close for closing price for a certain symbol and it gets the last element in the series
        volume = data['Volume'][symbol].iloc[-1] #inside the data we are accessing the column of volume for volume and .iloc[-1] - used to access the last element in the series
        prev_close = data['Close'][symbol].iloc[-2] #inside the data we are accessing the column of close but for the previous day hence .iloc[-2]
        change_pct = ((latest_data - prev_close) / prev_close) * 100
        stock_details = {
            "symbol" : symbol,
            "price" :  latest_data,
            "volume" : volume,
            "change_pct" : change_pct
        }
        stock_data_list.append(stock_details)
        with sqlite3.connect("database_db.db") as db :
            cursor = db.cursor()
            for stock in stock_data_list :
                cursor.execute(
                    '''
                    INSERT OR IGNORE INTO stock_market (symbol,price,volume,change_pct)
                    VALUES (?,?,?,?)
                    ''',(stock['symbol'], stock['price'], stock['volume'], stock['change_pct']) #tuple
                )
            db.commit()
            db.close()

            
fetch_data()

