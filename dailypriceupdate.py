import sqlite3
import pandas as pd
import yfinance as yf
import datetime as dt
from datetime import date



df_tickers = pd.read_csv(r'C:\Users\Antriksh Kandhari\Desktop\tradingdashboard\ITOT_holdings.csv')
tickers = df_tickers['Ticker'].tolist()


def dailypriceupdate(tickers):

    end =  dt.datetime.today()
    start = end - dt.timedelta(days=1)

    conn = sqlite3.connect('pricedata.db')

    c = conn.cursor()

    for i in tickers:

        try:

            df = yf.download(i, start = start, end = end)

            for index, row in df.iterrows():

                c.execute('''
                    INSERT or IGNORE INTO pricedata (Date, Ticker, Open, High, Low, Close, Volume)
                    VALUES (?,?,?,?,?,?,?)
                ''', (index.strftime('%Y-%m-%d'), i, row['Open'], row['High'], row['Low'], row['Adj Close'], row['Volume']))

        except Exception as e:
            print(e)

    conn.commit()
    conn.close()







