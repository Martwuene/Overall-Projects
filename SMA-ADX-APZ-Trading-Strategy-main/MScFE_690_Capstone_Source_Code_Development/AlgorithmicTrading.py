#!/usr/bin/env python
# coding: utf-8

def SMA_CrossOver(price, short_sma, long_sma):
    
    """ Creating a trading strategy of simple moving average crossover """
    
    # Import numpy
    import numpy as np
    
    sma1 = short_sma
    sma2 = long_sma
    sma_buy = []
    sma_sell = []
    sma_signal = []
    signal = 0
    
    for i in range(len(price)):
        if sma1[i] > sma2[i]:
            if signal != 1:
                sma_buy.append(price[i])
                sma_sell.append(np.nan)
                signal = 1
                sma_signal.append(signal)
            else:
                sma_buy.append(np.nan)
                sma_sell.append(np.nan)
                sma_signal.append(0)
        elif sma2[i] > sma1[i]:
            if signal != -1:
                sma_buy.append(np.nan)
                sma_sell.append(price[i])
                signal = -1
                sma_signal.append(-1)
            else:
                sma_buy.append(np.nan)
                sma_sell.append(np.nan)
                sma_signal.append(0)
        else:
            sma_buy.append(np.nan)
            sma_sell.append(np.nan)
            sma_signal.append(0)
            
    return sma_buy, sma_sell, sma_signal


def ADX(price, indicator, pos_indicator, neg_indicator):
    
    """ Creating an trading strategy of average directional index """
    
    # Import numpy
    import numpy as np
    
    adx_buy = []
    adx_sell = []
    adx_signal = []
    signal = 0
    
    for i in range(len(price)):
        if indicator[i-1] < 25 and indicator[i] > 25 and pos_indicator[i] > neg_indicator[i]:
            if signal != 1:
                adx_buy.append(price[i])
                adx_sell.append(np.nan)
                signal = 1
                adx_signal.append(signal)
            else:
                adx_buy.append(np.nan)
                adx_sell.append(np.nan)
                adx_signal.append(0)
        elif indicator[i-1] < 25 and indicator[i] > 25 and neg_indicator[i] > pos_indicator[i]:
            if signal != -1:
                adx_buy.append(np.nan)
                adx_sell.append(price[i])
                signal = -1
                adx_signal.append(signal)
            else:
                adx_buy.append(np.nan)
                adx_sell.append(np.nan)
                adx_signal.append(0)
        else:
            adx_buy.append(np.nan)
            adx_sell.append(np.nan)
            adx_signal.append(0)
            
    return adx_buy, adx_sell, adx_signal



def APZ(price, indicator, lowerband, upperband):
    
    """ Creating a trading strategy adaptive price zone """
    
    # Import numpy
    import numpy as np
    
    apz_buy = []
    apz_sell = []
    apz_signal = []
    signal = 0
    
    for i in range(len(price['Close'])):
        if indicator[i] <= 30:
            if price['Low'][i] <= lowerband[i]:
                if signal != 1:
                    apz_buy.append(price['Close'][i])
                    apz_sell.append(np.nan)
                    signal = 1
                    apz_signal.append(signal)
                else:
                    apz_buy.append(np.nan)
                    apz_sell.append(np.nan)
                    apz_signal.append(0)
           
            elif price['High'][i] >= upperband[i]:
                if signal != -1:
                    apz_buy.append(np.nan)
                    apz_sell.append(price['Close'][i])
                    signal = -1
                    apz_signal.append(-1)
                else:
                    apz_buy.append(np.nan)
                    apz_sell.append(np.nan)
                    apz_signal.append(0)
            else:
                apz_buy.append(np.nan)
                apz_sell.append(np.nan)
                apz_signal.append(0)
                    
        elif indicator[i] > 30:
            if price['High'][i] >= upperband[i]:
                if signal != 1:
                    apz_buy.append(price['Close'][i])
                    apz_sell.append(np.nan)
                    signal = 1
                    apz_signal.append(signal)
                else:
                    apz_buy.append(np.nan)
                    apz_sell.append(np.nan)
                    apz_signal.append(0)
           
            elif price['Low'][i] <= lowerband[i]:
                if signal != -1:
                    apz_buy.append(np.nan)
                    apz_sell.append(price['Close'][i])
                    signal = -1
                    apz_signal.append(-1)
                else:
                    apz_buy.append(np.nan)
                    apz_sell.append(np.nan)
                    apz_signal.append(0)
            else:
                apz_buy.append(np.nan)
                apz_sell.append(np.nan)
                apz_signal.append(0)
        else:
            apz_buy.append(np.nan)
            apz_sell.append(np.nan)
            apz_signal.append(0)
            
    return apz_buy, apz_sell, apz_signal


def SMA_ADX_APZ(price, short_sma, long_sma, indicator, pos_indicator, neg_indicator, lowerband, upperband):
    
    """ Creating a trading strategy of simple moving average crossover """
    
    # Import numpy
    import numpy as np
    
    sma1 = short_sma
    sma2 = long_sma
    buy = []
    sell = []
    signal = []
    signal_ = 0
    
    for i in range(len(price['Close'])):
        if sma1[i] > 25 and indicator[i-1] < 25 and indicator[i] > sma2[i] and 30 > neg_indicator[i] and indicator[i] < pos_indicator[i]:
            if price['Low'][i] <= lowerband[i]:
                if signal_ != 1:
                    buy.append(price['Close'][i])
                    sell.append(np.nan)
                    signal_ = 1
                    signal.append(signal)
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
                    signal.append(0)
           
            elif price['High'][i] >= upperband[i]:
                if signal_ != -1:
                    buy.append(np.nan)
                    sell.append(price['Close'][i])
                    signal_ = -1
                    signal.append(-1)
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
                    signal.append(0)
            else:
                buy.append(np.nan)
                sell.append(np.nan)
                signal.append(0)
                
        elif sma2[i] > 25 and indicator[i-1] < 25 and indicator[i] > sma1[i] and neg_indicator[i] > 30 and indicator[i] > pos_indicator[i]:
            if price['High'][i] >= upperband[i]:
                if signal_ != 1:
                    buy.append(price['Close'][i])
                    sell.append(np.nan)
                    signal_ = 1
                    signal.append(signal)
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
                    signal.append(0)
           
            elif price['Low'][i] <= lowerband[i]:
                if signal_ != -1:
                    buy.append(np.nan)
                    sell.append(price['Close'][i])
                    signal_ = -1
                    signal.append(-1)
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
                    signal.append(0)
            else:
                buy.append(np.nan)
                sell.append(np.nan)
                signal.append(0)
        else:
            buy.append(np.nan)
            sell.append(np.nan)
            signal.append(0)
            
    return buy, sell, signal