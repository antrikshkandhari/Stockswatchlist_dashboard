import sqlite3
import pandas as pd
import datetime as dt
from datetime import date

conn = sqlite3.connect('pricedata.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS etfs
    (Ticker text, Name text, Category text, PRIMARY KEY (Ticker))
''')

df = pd.read_csv(r'C:\Users\Antriksh Kandhari\Desktop\tradingdashboard\ETFs.csv')

for index, row in df.iterrows():

    c.execute('''
    INSERT OR IGNORE INTO etfs (Ticker, Name, Category)
    VALUES (?,?,?)
    ''', (row['Ticker'], row['Name'], row['Category']))


conn.commit()
conn.close()


