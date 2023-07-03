import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import math
from datetime import date
import sqlite3
from indicators import technicalindicators



df_tickers = pd.read_csv(r'C:\Users\Antriksh Kandhari\Desktop\tradingdashboard\ITOT_holdings.csv')
tickers = df_tickers['Ticker'].tolist()


def weeklyttm(tickers):

    now = date.today()

    weeklyttm = pd.DataFrame(columns=['Ticker', 'Last Price', '1day %', '7day %', '30day %', 'Momentum Score', 'RS', 'Volume %', "BBUP","BBDOWN", "KKUP","KKDOWN", 'ATR'])


    for i in tickers:

        try:
        
            df = yf.download(i, interval='1wk', period='1y')

            indicator = technicalindicators(df)
            new_row = pd.DataFrame([{'Ticker': i,
                                'Last Price': df['Close'].iloc[-1],
                                '1day %': indicator.returns(1),
                                '7day %': indicator.returns(7),
                                '30day %':indicator.returns(30),
                                'Momentum Score': indicator.momentum(1, 7, 30),
                                'RS': indicator.rs(14),
                                'Volume %': indicator.volumnechange(20, 7),
                                'BBUP': indicator.upperband(20, 2),
                                'BBDOWN': indicator.lowerband(20, 2),
                                'KKUP': indicator.upperchannel(20, 1.5),
                                'KKDOWN':indicator.lowerchannel(20, 1.5),
                                'ATR': indicator.atr(14)}])
        
        except Exception as e:
            print(e)

        weeklyttm = pd.concat([weeklyttm, new_row], ignore_index= True)

    weeklyttm['TTM'] = np.where((weeklyttm['BBUP'] < weeklyttm['KKUP']) & (weeklyttm['BBDOWN']> weeklyttm['KKDOWN']), True, False)  
    weeklyttm['Rank'] = weeklyttm['Momentum Score'].rank()
    weeklyttm = weeklyttm.drop([ "BBUP","BBDOWN", "KKUP","KKDOWN"], axis = 1)
    weeklyttm = weeklyttm.sort_values('Rank', ascending=False)

    filename = str(now) +"weeklybreakout.xlsx"
    weeklyttm.to_excel(filename, index = False)


weeklyttm(tickers=tickers)

