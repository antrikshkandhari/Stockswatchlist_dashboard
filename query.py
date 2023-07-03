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

query_indicatordata = '''Select t1.* from indicatorsdata as t1
                         Join (SELECT ticker, MAX(date) as max_date from indicatorsdata
                         GROUP BY ticker)
                         as t2 on t1.ticker = t2.ticker and t1.date = t2.max_date'''

breakoutcandidates = pd.read_sql_query(query_indicatordata, conn)
breakoutcandidates = pd.read_sql_query(query_indicatordata, conn)
breakoutcandidates['TTM'] = np.where((breakoutcandidates['BBUP'] < breakoutcandidates['KKUP']) & (breakoutcandidates['BBDOWN']> breakoutcandidates['KKDOWN']), True, False)  
breakoutcandidates['Rank'] = breakoutcandidates['MomentumScore'].rank()
breakoutcandidates = breakoutcandidates.drop([ "BBUP","BBDOWN", "KKUP","KKDOWN"], axis = 1)
breakoutcandidates = breakoutcandidates.sort_values('Rank', ascending=False)

print(breakoutcandidates)

conn.close()    

