#!/usr/bin/env python
# coding: utf-8

def SMA(price, short_sma, long_sma):
    
    """ Generate a plot of close prices and the simple moving average indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt

    # Plotting the price and simple moving average
    fig = plt.figure(figsize=(18,7))
    ax1 = plt.plot(price['Close'])
    ax1 = plt.plot(short_sma)
    ax1 = plt.plot(long_sma)
    ax1 = plt.title('Gold Daily Close Price and Simple Moving Average (200-day)', fontsize=18)
    ax1 = plt.xlabel('Date')
    ax1 = plt.ylabel('Price ($)')
    ax1 = plt.legend(['Price', 'SMA 20', 'SMA 200'])
    plt.show()
    
def MACD(price, indicator, signal, hist):
    
    """ Generate a plot of close prices and the moving average convergence divergence indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting the price and moving average convergence divergence
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 3, colspan = 1, sharex=ax1)

    ax1.plot(price['Close'])
    ax2.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    ax2.plot(indicator, color = 'orange', linewidth = 1.5, label = 'MACD')
    ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(price)):
        if str(hist[i])[0] == '-':
            ax2.bar(price.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(price.index[i], hist[i], color = '#26a69a')
    ax1.set_title('Gold Daily Close Price')
    ax2.set_title('Moving Average Convergence Divergence')        
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.grid(False)
    plt.legend(loc = 'lower right')
    plt.gcf().set_size_inches(18,9)
    
def RSI(price, indicator):
    
    """ Generate a plot of close prices and the relative strength index indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting the price and relative strength index
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 3, colspan = 1, sharex=ax1)

    ax1.plot(price['Close'])
    ax2.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    ax2.set_ylabel('(%)')
    ax2.plot(price.index, [70] * len(price.index), label="overbought")
    ax2.plot(price.index, [30] * len(price.index), label="oversold")
    ax2.plot(price.index, indicator, label="rsi")
    ax1.set_title('Gold Daily Close Price')
    ax2.set_title('Relative Strength Index')
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.grid(False)
    ax2.legend(bbox_to_anchor=(1,1), loc=2, borderaxespad=0.)
    plt.gcf().set_size_inches(18,9)
    
def StochasticOscillator(price, slowk, slowd):
    
    """ Generate a plot of close prices and the stochastic oscillator indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting price and stochastic oscillator
    ax1 = plt.subplot2grid((9, 1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10, 1), (6,0), rowspan = 3, colspan = 1)
    ax1.plot(price['Close'])
    ax2.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    
    ax2.plot(slowk, color = 'deepskyblue', linewidth = 1.5, label = '%K')
    ax2.plot(slowd, color = 'orange', linewidth = 1.5, label = '%D')
    ax2.axhline(80, color = 'black', linewidth = 1, linestyle = '--')
    ax2.axhline(20, color = 'black', linewidth = 1, linestyle = '--')
    ax1.set_title('Gold Daily Close Price')
    ax2.set_title('Stochastic Oscillator')
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.grid(False)
    ax2.legend(loc = 'lower right')
    plt.gcf().set_size_inches(18,9)
    
def BollingerBands(price, upperband, middleband, lowerband):
    
    """ Generate a plot of close prices and the bollinger bands indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting price and bollinger bands
    fig = plt.figure(figsize=(18,9))
    ax1 = plt.plot(price['Close'], linewidth = 2)
    ax1 = plt.plot(upperband, c='green')
    ax1 = plt.plot(middleband, c='darkorange')
    ax1 = plt.plot(lowerband, c='red')
    ax1 = plt.title('Gold Daily Close Price and Bollinger Bands', fontsize=18)
    ax1 = plt.xlabel('Date', fontsize=15)
    ax1 = plt.ylabel('Price ($)', fontsize=15)
    ax1 = plt.legend(['Price', 'Upperband', '200-day SMA', 'Lowerband'])
    plt.grid(True)
    plt.show()

def OBV(price, indicator):
    
    """ Generate a plot of close prices and the on-balance volume indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting price and on-balance volume
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 3, colspan = 1, sharex=ax1)
    ax1.plot(price['Close'], linewidth = 2)
    ax2.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    ax2.plot(price.index, indicator, color= 'red', linewidth = 2)
    ax1.set_title('Gold Daily Close Price')
    ax2.set_title('On-Balance Volume')
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.grid(False)
    plt.gcf().set_size_inches(18,9)
    
def ATR(price, indicator):
    
    """ Generate a plot of close prices and the average true range indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting price and average true range
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 3, colspan = 1, sharex=ax1)
    ax1.plot(price['Close'], linewidth = 2)
    ax2.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    ax2.plot(price.index, indicator, color= 'red', linewidth = 2)
    ax1.set_title('Gold Daily Close Price')
    ax2.set_title('Average True Range')
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.grid(False)
    plt.gcf().set_size_inches(18,9)
    
def ADX(price, indicator, pos_indicator, neg_indicator):
    
    """ Generate a plot of close prices and the average directional index indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting the price and average directional index
    ax1 = plt.subplot2grid((9,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 3, colspan = 1, sharex=ax1)
    
    ax1.plot(price['Close'])
    ax2.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    ax2.plot(pos_indicator, color = '#26a69a', label = '+ DI 14', linewidth = 2, alpha = 0.3)
    ax2.plot(neg_indicator, color = '#f44336', label = '- DI 14', linewidth = 2, alpha = 0.3)
    ax2.plot(indicator, color = '#2196f3', label = 'ADX 14', linewidth = 2)
    ax2.axhline(25, color = 'grey', linewidth = 2, linestyle = '--')
    ax1.set_title('Gold Daily Close Price', fontsize=18)
    ax2.set_title('Average Directional Index')
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax2.legend()
    ax2.legend(bbox_to_anchor=(1,1), loc=2, borderaxespad=0.)
    plt.gcf().set_size_inches(18,9)
    
def APZ(price, lowerband, upperband):
    
    """ Generate a plot of close prices and the adaptive price zone indicator """
    
    # Import matplotlib.pyplot
    import matplotlib.pyplot as plt
    
    # Plotting price and APZ bands
    fig = plt.figure(figsize=(18,7))
    ax1 = plt.plot(price['Close'])
    ax1 = plt.plot(upperband, c='green')
    ax1 = plt.plot(lowerband, c='red')
    ax1 = plt.title('Gold Daily Close Price and Adaptive Price Zone', fontsize=18)
    ax1 = plt.xlabel('Date')
    ax1 = plt.ylabel('Price ($)')
    ax1 = plt.legend(['Price', 'Upper APZ Band', 'Lower APZ Band'])
    plt.grid(True)
    plt.show() 