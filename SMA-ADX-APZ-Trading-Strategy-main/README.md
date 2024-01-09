# Algorithmic Trading for Long-Term Trends in Commodities Markets
Developing an expanded or upgraded algorithmic trading strategy for trend-following strategies, which were previously trading orders for long-term trends in commodity futures markets, in order to recognize and validate time, price, and volume using automated techniques. This trading requirement takes advantage of algorithms' intensity and handling bandwidth by combining the selected strategies that are to be used before they are all combined so that they can trade in all trends (bullish and bearish markets), including choppy markets, which are the Simple Moving Average Crossover Strategy, Average Directional Index Strategy, and Adaptive Price Zone Strategy. 

# Technical Indicators
1. [Simple Moving Average (SMA)](https://www.investopedia.com/terms/s/sma.asp) is a mathematical moving average that is calculated by multiplying current prices by the number of time periods in the computation average. 

2. [Average Directional Index (ADX)](https://www.investopedia.com/terms/a/adx.asp) is a technical analysis indicator employed by some traders to gauge the strength of a trend. Two complementing indicators, the negative directional indicator (-DI) and the positive directional indicator (+DI), reveal whether the trend is up or down.

3. [Adaptive Price Zone (APZ)](https://www.investopedia.com/terms/a/adaptive-price-zone.asp) is a volatility-based technical indicator that can help investors spot potential market turning points, which is particularly valuable in a sideways market. 

# Algorithmic Trading
Before backtesting these strategies in order to compare them to the simple moving average crossover strategy as a trend indicator, all of the above-mentioned indicators will be integrated to form a single trading strategy.
The results would be significant, and we might be able to eliminate one of the most prevalent issues with technical indicators, namely misleading signals. 

# Performance Statistics
The effectiveness of an algorithm is evaluated in contrast to another technique that addresses the same application difficulty. Programmers can use efficient algorithms to create better and more efficient algorithms. Most experienced institutional investors would use the pyfolio package to evaluate the algorithm's success because it contains a wealth of performance data. These indicators include the algorithm's daily, monthly, and yearly returns, yield summary data, and sharpe ratios, as well as the portfolio's volatility. The most significant metrics to evaluate in a data frame are the ones listed below. 


To construct our algorithmic trading in our research, we used daily prices of one of the following precious metals and commodities: Gold, silver, platinum, palladium download from [Investing.com](https://www.investing.com/).

# Installing

Install required libraries.

    $pip install -r requirements.txt
    
If TA-LIB struggles to install on the macOS M1 chip on the terminal, try the following instructions.

    $conda install -c conda-forge ta-lib 
    
If it is still not working, try another option to follow the steps on this link, [Quantinsti](https://blog.quantinsti.com/install-ta-lib-python/).

    $brew install ta-lib

# Running
Run only one Jupyter Notebook file on a local machine.

    Long-term Trends in Commodity Future Markets.ipynb
