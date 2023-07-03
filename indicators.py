import pandas as pd
import numpy as np

class technicalindicators:
    def __init__(self, df):
        self.df = df

    def rs(self, window=14):
        
        price_diff = self.df['Close'].diff(1)
        gain = price_diff.where(price_diff > 0, 0)
        loss = -price_diff.where(price_diff < 0, 0)
        
        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()
        
        rs = (avg_gain / avg_loss).round(2)
        
        return rs.iloc[-1]
    
    def ma(self, window):

        ma = (self.df['Close'].rolling(window).mean()).round(2)

        return ma.iloc[-1]
    
    def ema(self, window):

        ema = (self.df['Close'].ewm(span= window, adjust= False).mean()).round(2)

        return ema.iloc[-1]
    
    def atr(self, window=20):

        tr = abs(self.df['High'] - self.df['Low'])
        atr = (tr.rolling(window).mean()).round(2)

        return atr.iloc[-1]
    
    def upperband(self, window=20, num_std=2):

        mean = self.ma(window=window)
        std = self.df['Close'].rolling(window).std()

        upperband = (mean + (num_std * std)).round(2)

        return upperband.iloc[-1]

    def lowerband(self, window=20, num_std=2):

        mean = self.ma(window=window)
        std = self.df['Close'].rolling(window).std()

        lowerband = (mean - (num_std * std)).round(2)    

        return lowerband.iloc[-1]
        
    
    def lowerchannel(self, window=20, multiplier = 1.5):

        ma = self.ma(window=window)
        atr = self.atr(window=window)

        lowerchannel = ma - (multiplier * atr)

        return lowerchannel

    def upperchannel(self, window=20, multiplier = 1.5):

        ma = self.ma(window=window)
        atr = self.atr(window=window)

        upperchannel = ma + (multiplier * atr)     

        return upperchannel
    
    def returns(self, days):

        returns =((self.df['Close'].pct_change(periods =days)) *100).round(2)

        return returns.iloc[-1]
    
    def momentum(self,a, b, c ):

        momentum = ((self.returns(a) * .40)+ (self.returns(b)*.35) + (self.returns(c) *.25)).round(2)

        return momentum
    
    def volumnechange(self, window, days):

        volumema = (self.df['Volume'].rolling(window).mean()).round(2)

        volumechange = ((volumema.pct_change(periods = days )) *100).round(2)

        return volumechange.iloc[-1]



    








    
    

    


