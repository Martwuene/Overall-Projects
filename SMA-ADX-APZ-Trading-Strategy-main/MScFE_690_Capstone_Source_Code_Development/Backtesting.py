#!/usr/bin/env python
# coding: utf-8

# Import math
import math
# Import numpy
import numpy as np
# Import pandas
import pandas as pd
# Import colored 
from termcolor import colored as cl 
    

def implementation(price, strategy_df, investment_value, name):
    
    """ Building the backtesting in investing the certain capital to invest in the implemented strategies. """
    
    # Backtesting implementation
    # Create price difference
    commodity_return = pd.DataFrame(np.diff(price['Close'])).rename(columns = {0:'return'})
    # Create an empty list for strategy return
    strategy_return = []

    for i in range(len(commodity_return)):
        return_of_strategy = commodity_return['return'][i] * strategy_df['position'][i]
        strategy_return.append(return_of_strategy)
     
    # Create data-frame for strategy return and rename a column
    strategy_return_df = pd.DataFrame(strategy_return).rename(columns = {0:'strategy_return'})
    # Compute number of shares
    number_of_shares = math.floor(investment_value/price['Close'][-1])
    # Create an empty list for investment strategy return
    strategy_investment_return = []

    for i in range(len(strategy_return_df['strategy_return'])):
        return_of_investment = number_of_shares * strategy_return_df['strategy_return'][i]
        strategy_investment_return.append(return_of_investment)
        
    # Create data-frame for investment strategy return and rename a column
    investment_return_df = pd.DataFrame(strategy_investment_return).rename(columns = {0:'investment_return'})
    # Compute the total investment return
    total_investment_return = round(sum(investment_return_df['investment_return']), 2)
    # Compute the percentage of investment return
    profit_percentage = math.floor((total_investment_return/investment_value)*100)
    
    if total_investment_return < 0:
        print(cl('Profit loss from the '+ str(name) +' strategy by investing $'+str(math.floor(investment_value/1000))+'K in Gold : ${}'.format(abs(total_investment_return)), 
             attrs = ['bold']))
        print(cl('Profit percentage of the '+ str(name) +' strategy : {}%'.format(profit_percentage), attrs = ['bold']))
        
    else:
        print(cl('Profit gained from the '+ str(name) +' strategy by investing $'+str(math.floor(investment_value/1000))+'K in Gold : ${}'.format(total_investment_return), 
             attrs = ['bold']))
        print(cl('Profit percentage of the '+ str(name) +' strategy : {}%'.format(profit_percentage), attrs = ['bold']))