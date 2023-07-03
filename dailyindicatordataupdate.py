import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import math
from datetime import date
import sqlite3
from indicators import technicalindicators

now = date.today()

df_tickers = pd.read_csv(r'C:\Users\Antriksh Kandhari\Desktop\tradingdashboard\ITOT_holdings.csv')
tickers = df_tickers['Ticker'].tolist()

#tickers = ['SPY']
def indicatordata(tickers):
    now = date.today()


    breakoutcandidates = pd.DataFrame(columns=['Ticker', 'Last Price', '1day %', '7day %', '30day %','MA 50','MA 200', 'Momentum Score', 'RS', 'Volume %', "BBUP","BBDOWN", "KKUP","KKDOWN", 'ATR'])

    conn = sqlite3.connect('pricedata.db')

    c = conn.cursor()

    c.execute('''
        CREATE Table if not exists indicatorsdata 
        (Date text, Ticker text, Last_Price real, day1 real , day7 real, day30 real , MA50 real, MA200 real, MomentumScore real, RS real, Volume real,BBUP real,BBDOWN real, KKUP real,KKDOWN real, ATR real, PRIMARY KEY (date, ticker))            
    ''')

    for i in tickers:

        try:
        
            query = f'SELECT * from pricedata where Ticker ="{i}" ORDER by Date ASC'
            df = pd.read_sql_query(query, conn)
            print(df)   
            indicator = technicalindicators(df)
            new_row = pd.DataFrame([{'Ticker': i,
                                'Last Price': df['Close'].iloc[-1],
                                '1day %': indicator.returns(1),
                                '7day %': indicator.returns(7),
                                '30day %':indicator.returns(30),
                                'MA 50': indicator.ma(50),
                                'MA 200': indicator.ma(200),
                                'Momentum Score': indicator.momentum(1, 7, 30),
                                'RS': indicator.rs(14),
                                'Volume %': indicator.volumnechange(20, 7),
                                'BBUP': indicator.upperband(20, 2),
                                'BBDOWN': indicator.lowerband(20, 2),
                                'KKUP': indicator.upperchannel(20, 1.5),
                                'KKDOWN':indicator.lowerchannel(20, 1.5),
                                'ATR': indicator.atr(14)}])
            
            c.execute('''
                INSERT or IGNORE INTO indicatorsdata (Date ,Ticker,Last_price , day1  , day7 , day30  , MA50 , MA200 , MomentumScore , RS , Volume,BBUP,BBDOWN, KKUP,KKDOWN , ATR)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (now,i,df['Close'].iloc[-1],indicator.returns(1),indicator.returns(7),indicator.returns(30),indicator.ma(50),indicator.ma(200),indicator.momentum(1, 7, 30),indicator.rs(14),indicator.volumnechange(20, 7),indicator.upperband(20, 2),indicator.lowerband(20, 2),indicator.upperchannel(20, 1.5),indicator.lowerchannel(20, 1.5),indicator.atr(14)))

            conn.commit()
        except Exception as e:
            print(e)

        breakoutcandidates = pd.concat([breakoutcandidates, new_row], ignore_index= True)


    breakoutcandidates['TTM'] = np.where((breakoutcandidates['BBUP'] < breakoutcandidates['KKUP']) & (breakoutcandidates['BBDOWN']> breakoutcandidates['KKDOWN']), True, False)  
    breakoutcandidates['Rank'] = breakoutcandidates['Momentum Score'].rank()
    breakoutcandidates = breakoutcandidates.drop([ "BBUP","BBDOWN", "KKUP","KKDOWN"], axis = 1)
    breakoutcandidates = breakoutcandidates.sort_values('Rank', ascending=False)

    filename = str(now) +"breakout.xlsx"
    breakoutcandidates.to_excel(filename, index = False)

    conn.close()