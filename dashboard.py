import pandas as pd
import numpy as np
import sqlite3
import datetime 
from datetime import date
import streamlit as st
import csv
import requests

conn = sqlite3.connect('pricedata.db')

c = conn.cursor()

query_forstockinfo = 'Select * from stockinfo'

dfinfo = pd.read_sql_query(query_forstockinfo, conn)

query_indicatordata = '''SELECT t1.* FROM indicatorsdata as t1
                         JOIN (SELECT ticker, MAX(date) as max_date from indicatorsdata
                         GROUP BY ticker)
                         as t2 ON t1.ticker = t2.ticker AND t1.date = t2.max_date'''

breakoutcandidates = pd.read_sql_query(query_indicatordata, conn)
breakoutcandidates['TTM'] = np.where((breakoutcandidates['BBUP'] < breakoutcandidates['KKUP']) & (breakoutcandidates['BBDOWN']> breakoutcandidates['KKDOWN']), True, False)  
breakoutcandidates['Rank'] = breakoutcandidates['MomentumScore'].rank()
breakoutcandidates = breakoutcandidates.drop([ "BBUP","BBDOWN", "KKUP","KKDOWN"], axis = 1)
breakoutcandidatesdf = breakoutcandidates.sort_values('Rank', ascending=False)

# Add a page for Notes for watchlist items
pages =  ['Dashboard','Charts for Momentum', 'Charts for TTM', 'Charts for TTM Weekly', 'ETFs',  'Charts for Top Caps','Relative Strength', 'Watchlist']
page = st.selectbox('Menu:', pages)


if page == 'Dashboard':
    st.header("KPI")
    df = breakoutcandidatesdf

    pctupdown = st.number_input('Stocks up and down daily:', 4 )

    num_ticker_above  =len(df[df['day1']> pctupdown])
    st.write(f'Number of stocks up: {num_ticker_above}')

    num_ticker_below  =len(df[df['day1']< (-(pctupdown))])
    st.write(f'Number of stocks down : {num_ticker_below}')

    pctupdown30 = st.number_input('Stocks up and down 30day:', 25 )


    num_ticker_above  =len(df[df['day30']> pctupdown30])
    st.write(f'Number of stocks up: {num_ticker_above}')

    num_ticker_below  =len(df[df['day30']< (-(pctupdown30))])
    st.write(f'Number of stocks down : {num_ticker_below}')

    ttm  =len(df[df['TTM'] == True])
    st.write(f'Number of stocks in TTM: {ttm}')

    rs  =(df['RS'].mean()).round(2)
    st.write(f'Average RS is {rs}')


    ma  =len(df[df['MA200'] <df['Last_Price']])
    st.write(f'Above Moving Average {ma}')


    st.dataframe(df)



elif page == 'Charts for Momentum':

    df = breakoutcandidatesdf
    df.drop_duplicates(subset=['Ticker'])
    df2 = df.head(100)
    tickers = df2['Ticker'].tolist()

    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []

    for ticker in tickers:
        try:
            st.image(f'https://charts2.finviz.com/chart.ashx?t={ticker}') 
            rs =df[df['Ticker']==ticker]['RS']
            st.write(rs)
            industry = dfinfo[dfinfo['Ticker'] ==ticker]['Industry']
            st.write(industry)
            summary = dfinfo[dfinfo['Ticker'] ==ticker]['Summary']
            st.write(summary)

            
            if ticker not in st.session_state.watchlist:
                if st.button(f'Add {ticker} to watchlist'):
                    st.session_state.watchlist.append(ticker)
                    

        except Exception:
            pass

    with open('watchlist.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(st.session_state.watchlist)

elif page == 'Charts for TTM':
    st.header('Only TTM Stocks')
    df = breakoutcandidatesdf
    df.drop_duplicates(subset=['Ticker'])
    df3 = (df[df['TTM']==True])
    dfma = df3[df3['Last_Price'] > df3['MA200']]
    dfrs = dfma.sort_values('RS', ascending= False)
    tick = dfrs.head(100)
    ticker = tick['Ticker'].tolist()
    

    for i in ticker:
        try:
            st.image(f'https://charts2.finviz.com/chart.ashx?t={i}')
            rs =df[df['Ticker']==i]['RS']
            st.write(rs)
            industry = dfinfo[dfinfo['Ticker'] ==i]['Industry']
            st.write(industry)
            summary = dfinfo[dfinfo['Ticker'] ==i]['Summary']
            st.write(summary)

            


            if i not in st.session_state.watchlist:
                    if st.button(f'Add {i} to watchlist'):
                        st.session_state.watchlist.append(i)
                        

        except Exception:
            pass

    with open('watchlist.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(st.session_state.watchlist)

elif page == 'Charts for TTM Weekly':

    st.header('Only TTM weekly Stocks')
    df = breakoutcandidatesdf
    df.drop_duplicates(subset=['Ticker'])
    df3 = (df[df['TTM']==True])
    dfrs = df3.sort_values('RS', ascending= False)
    tick = dfrs['Ticker'].tolist()
    

    for i in tick:
        try:
            st.image(f'https://charts2.finviz.com/chart.ashx?t={i}')
            rs =df[df['Ticker']==i]['RS']
            st.write(rs)
            industry = dfinfo[dfinfo['Ticker'] ==i]['Industry']
            st.write(industry)
            summary = dfinfo[dfinfo['Ticker'] ==i]['Summary']
            st.write(summary)

            


            if i not in st.session_state.watchlist:
                    if st.button(f'Add {i} to watchlist'):
                        st.session_state.watchlist.append(i)
                        

        except Exception:
            pass

    with open('watchlist.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(st.session_state.watchlist)


elif page == 'ETFs':
    
    query = ("SELECT * from etfs")
    df = pd.read_sql_query(query, conn)

    tickers = df['Ticker'].tolist()

    for i in tickers:

        st.image(f'https://charts2.finviz.com/chart.ashx?t={i}')
        st.write(df[df['Ticker']==i]['Name'])
        st.write(df[df['Ticker']==i]['Category'])




elif page == 'Charts for Top Caps':
    
    query = ("SELECT * from companyinfo order by MarketCap DESC")
    df = pd.read_sql_query(query, conn)
   
    df32 = df.head(100)

    tickers = df32['Ticker'].tolist()

    for i in tickers:

        st.image(f'https://charts2.finviz.com/chart.ashx?t={i}')



elif page == 'Relative Strength':
    df = breakoutcandidatesdf

    a = st.text_input('Add Ticker:', )
    b = st.text_input('Add Ticker to compare:', )
    
    col1, col2 = st.columns(2)
    col1.image(f'https://charts2.finviz.com/chart.ashx?t={a}')

    rs =df[df['Ticker']==a]['RS']
    momentum = df[df['Ticker']==a]['MomentumScore']
    col1.write(rs)
    col1.write(momentum)

    industry = dfinfo[dfinfo['Ticker'] ==a]['Industry']
    col1.write(industry)
    summary = dfinfo[dfinfo['Ticker'] ==a]['Summary']
    col1.write(summary)

    col2.image(f'https://charts2.finviz.com/chart.ashx?t={b}')

    rs2 =df[df['Ticker']==b]['RS']
    momentum2 = df[df['Ticker']==b]['MomentumScore']
    col2.write(rs2)
    col2.write(momentum2)

    industry = dfinfo[dfinfo['Ticker'] ==b]['Industry']
    col2.write(industry)
    summary = dfinfo[dfinfo['Ticker'] ==b]['Summary']
    col2.write(summary)
    


elif page == 'Watchlist':

    st.header("Updated list from watchlist items")
    df_watchlist = pd.read_csv(r'watchlist.csv')
    df = breakoutcandidatesdf
    df4 = df_watchlist.columns.tolist()


    for i in df4:
        try:
            st.image(f'https://charts2.finviz.com/chart.ashx?t={i}')
            rs =df[df['Ticker']==i]['RS']
            st.write(rs)
            industry = dfinfo[dfinfo['Ticker'] ==i]['Industry']
            st.write(industry)
            summary = dfinfo[dfinfo['Ticker'] ==i]['Summary']
            st.write(summary)

            if i in st.session_state.watchlist:
                if st.button(f'Remove {i} from watchlist'):
                    st.session_state.watchlist.remove(i)


        except Exception as e:
            print("Nothing Here Yet")

    with open('watchlist.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(st.session_state.watchlist)   

