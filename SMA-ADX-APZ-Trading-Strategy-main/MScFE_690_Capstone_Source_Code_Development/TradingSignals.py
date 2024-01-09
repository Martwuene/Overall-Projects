#!/usr/bin/env python
# coding: utf-8

def SMA_Crossover(price, short_sma, long_sma, buy, sell):
    
    """ Generating a plot of trading signals with close prices and the simple moving average crossover strategy """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt

    # Plotting simple moving average crossover strategy trading signal
    fig = plt.figure(figsize=(18,7))
    plt.plot(price['Close'], alpha = 0.4, label = 'GOLD')
    plt.plot(short_sma, alpha = 0.6, label = 'SMA 20')
    plt.plot(long_sma, alpha = 0.6, label = 'SMA 200')
    plt.scatter(price.index, buy, marker = '^', s = 200, color = 'darkgreen', label = 'BUY SIGNAL')
    plt.scatter(price.index, sell, marker = 'v', s = 200, color = 'crimson', label = 'SELL SIGNAL')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend(loc = 'upper right')
    plt.title('Gold Simple Moving Average Crossover Trading Signals')
    plt.show()
    
    
def ADX(price, indicator, pos_indicator, neg_indicator, buy, sell):   
    
    """ Generating a plot of trading signals with close prices and the average directional index indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting the price and average directional index
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 3, colspan = 1, sharex=ax1)
    
    ax1.plot(price['Close'], alpha = 0.4, label = 'GOLD')
    ax2.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    ax1.scatter(price.index, buy, marker = '^', s = 200, color = 'darkgreen', label = 'BUY SIGNAL')
    ax1.scatter(price.index, sell, marker = 'v', s = 200, color = 'crimson', label = 'SELL SIGNAL')
    ax2.plot(pos_indicator, color = '#26a69a', label = '+ DI 14', linewidth = 2, alpha = 0.3)
    ax2.plot(neg_indicator, color = '#f44336', label = '- DI 14', linewidth = 2, alpha = 0.3)
    ax2.plot(indicator, color = '#2196f3', label = 'ADX 14', linewidth = 2)
    ax2.axhline(25, color = 'grey', linewidth = 2, linestyle = '--')
    ax1.set_title('Gold Average Directional Index Trading Signals')
    ax2.set_title('Average Directional Index')
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.legend(bbox_to_anchor=(1,1), loc=2, borderaxespad=0.)
    ax2.legend(bbox_to_anchor=(1,1), loc=2, borderaxespad=0.)
    plt.gcf().set_size_inches(18,9)

    
def APZ(price, lowerband, upperband, buy, sell):
    
    """ Generating a plot of trading signals with close prices and the adaptive price zone indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting price and bollinger bands
    fig = plt.figure(figsize=(18,7))
    ax1 = plt.plot(price['Close'], alpha = 0.4, label = 'GOLD')
    ax1 = plt.scatter(price.index, buy, marker = '^', s = 200, color = 'darkgreen', label = 'BUY SIGNAL')
    ax1 = plt.scatter(price.index, sell, marker = 'v', s = 200, color = 'crimson', label = 'SELL SIGNAL')
    ax1 = plt.plot(upperband, c='green', label='UPPER_APZ', alpha = 0.3)
    ax1 = plt.plot(lowerband, c='red', label='LOWER_APZ', alpha = 0.3)
    ax1 = plt.title('Gold Adaptive Price Zone Trading Signals')
    ax1 = plt.xlabel('Date')
    ax1 = plt.ylabel('Price ($)')
    ax1 = plt.legend()
    plt.grid(True)
    plt.show()