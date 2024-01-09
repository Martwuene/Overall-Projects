#import libraries
import pandas as pd
import numpy as np
import yfinance as yfin

import warnings
warnings.filterwarnings("ignore")

###############################################################################################################################
################################################## FINANCIAL INDICATORS #######################################################

def financial_indicators(balance, income, cashflow, ticker):
    
    # list of financial indicators from financial statements
    indicators = ['EBIT', 'OrdinarySharesNumber', 'CommonStock', 'CurrentAssets', 
                  'CurrentLiabilities', 'NetPPE', 'StockholdersEquity', 'LongTermDebt',
                  'TotalAssets', 'GrossProfit', 'TotalRevenue', 'depreciation', 
                  'totalCashFromOperatingActivities', 'NetIncome']
    
    # date-time for available stock price
    date = ['2022-04','2021-04','2020-04','2019-04']
    
    # for available financial years in financial statements
    year = [2022, 2021, 2020, 2019]
    
    # creat empty set to update nested dictionary
    nested_dict = {}
    
    for i in indicators:
        # create empty dictionary with empty lists
        dict_data = {2022:[], 2021:[], 2020:[], 2019:[]}
        for j, k in zip(range(len(ticker)), ticker):
            for l, m, n in zip(range(len(year)), year, date):
                
                # defaulted to extract from balance sheet
                if i in balance[j].index:
                    # extracting common stock
                    if i == 'CommonStock':
                        # extract closing stock price
                        price_data = yfin.Ticker(k+'.JO').history(period='5y')
                        if n in [str(x)[:7] for x in price_data.index]:
                            # compute/calculate market cap
                            marketcap = balance[j].loc[i][l]*\
                                        (price_data.loc[n+'-01':n+'-30']['Close'][0]/100)
                            dict_data[m].append(marketcap)
                        else:
                            dict_data[m].append(0)
                    else:    
                        ind = balance[j].loc[i][l]
                        dict_data[m].append(ind)
                        
                # defaulted to extract from income statement
                elif i in income[j].index:
                    ind = income[j].loc[i][l]
                    dict_data[m].append(ind)
                    
                else:
                    
                    # defaulted to extract from cashflow statement
                    ind = cashflow[j].loc[i][l]
                    dict_data[m].append(ind)
                    
        # update nested dictionary        
        nested_dict[i]= dict_data    
    
            
    # hierarchical indices and columns
    index = pd.MultiIndex.from_product([[2022, 2021, 2020, 2019],   ['EBIT',
                                                                     'OSN',
                                                                     'Market Cap',
                                                                     'TCA',
                                                                     'TCL',
                                                                     'PPE',
                                                                     'Book Value',
                                                                     'LTD',
                                                                     'Total Assets',
                                                                     'Gross Profit',
                                                                     'Total Revenue',
                                                                     'Depreciation',
                                                                     'TCFOA',
                                                                     'Net Income']],

                                   names=['year', ''])
    columns = pd.MultiIndex.from_product([ticker],
                                     names=['ticker'])
    
    # combining indicators from dictionary for each years
    collection = []
    for x in year:
        for y in nested_dict:
            collection.append(nested_dict[y][x])

    # mock some data
    data = np.array(collection)

    # create the DataFrame
    data = pd.DataFrame(data, index=index, columns=columns)
    
    return data

################################################################################################################################
################################################### FINANCIAL METRICS ##########################################################


def financial_metrics(df, ticker):
    
    # MAGIC FORMULA RANKING
    
    # list of financial metrics
    metrics = ['ev', 'wc', 'tev', 'ey', 'tc', 'roic']

    # for available financial years in financial statements
    year = [2022, 2021, 2020]
    
    # create empty set for nested dictionary
    nested_metric = {}
    
    for i in metrics:
        # create empty dictionary with empty lists
        dict_data = {2022:[], 2021:[], 2020:[]}
        for j in range(len(ticker)):
            for k in year:
                # compute enterprise value
                if i == 'ev':
                    ev = df.loc[(k, 'Market Cap')][j] + df.loc[(k, 'LTD')][j]
                    dict_data[k].append(ev)
                # compute working capital    
                elif i == 'wc':
                    wc = df.loc[(k, 'TCA')][j] + df.loc[(k, 'TCL')][j]
                    dict_data[k].append(wc)
                    
        # updating nested dictionary        
        nested_metric[i] = dict_data
        
    for i in metrics[2:]:
        # create empty dictionary with empty lists
        dict_data = {2022:[], 2021:[], 2020:[]}
        for j in range(len(ticker)):
            for k in year:
                # compute total enterprise value
                if i == 'tev':
                    tev = nested_metric['ev'][k][j] - nested_metric['wc'][k][j]
                    dict_data[k].append(tev)
                # compute earning yield    
                elif i == 'ey':
                    if nested_metric['tev'][k][j] == 0:
                        dict_data[k].append(nested_metric['tev'][k][j])
                    else:
                        ey = df.loc[(k, 'EBIT')][j] / nested_metric['tev'][k][j]
                        dict_data[k].append(ey)
                 # compute tangible capital        
                elif i == 'tc':
                    tc = nested_metric['wc'][k][j] + df.loc[(k, 'PPE')][j]
                    dict_data[k].append(tc)
                # compute return on invested capital   
                elif i == 'roic':
                    if nested_metric['tc'][k][j] == 0:
                        dict_data[k].append(nested_metric['tc'][k][j])
                    else:
                        roic = df.loc[(k, 'PPE')][j] / nested_metric['tc'][k][j]
                        dict_data[k].append(roic)
                    
        # updating nested dictionary            
        nested_metric[i] = dict_data 
        
        
    # PIOTROSKI F SCORE FACTORS
    
    # list of f-score factors
    factors = ['roa', 'cfo', 'droa', 'accrual', 'dlever', 'dliquid', 
               'eqo', 'dgm', 'dturn']

    for i in factors:
        # create empty dictionary with empty lists
        dict_data = {2022:[], 2021:[], 2020:[]}
        for j in range(len(ticker)):
            for k in year:
                # (1) Profitability
                # - return on assets. Net Income divided by year beginning total assets.
                if i == 'roa':
                    roa = int((df.loc[(k, 'Net Income')][j] / df.loc[(k, 'Total Assets')][j])  > 0)
                    dict_data[k].append(roa)
                    
                # - operating cash flow divided by year beginning total assets.
                elif i == 'cfo':
                    cfo = int((df.loc[(k, 'TCFOA')][j] / df.loc[(k, 'Total Assets')][j])  > 0) 
                    dict_data[k].append(cfo)
                    
                # - change in roa from the prior year.
                elif i == 'droa':
                    droa = int((df.loc[(k, 'Net Income')][j] / df.loc[(k, 'Total Assets')][j]) -\
                               (df.loc[(k-1, 'Net Income')][j] / df.loc[(k-1, 'Total Assets')][j]) > 0)
                    dict_data[k].append(droa)
   
                # - cfo compared to roa.
                elif i == 'accrual':
                     accrual = int((df.loc[(k, 'TCFOA')][j] / df.loc[(k, 'Total Assets')][j]) >\
                                   (df.loc[(k, 'Net Income')][j] / df.loc[(k, 'Total Assets')][j]))
                     dict_data[k].append(accrual)                
    
                # (2) Leverage, Liquidity, and Source of Funds
                # - change in long-term debt/average total assets ratio.
                elif i == 'dlever':
                    dlever = int(((df.loc[(k, 'LTD')][j] - df.loc[(k-1, 'LTD')][j])\
                                  / np.mean([df.loc[(k, 'Total Assets')][j], df.loc[(k-1, 'Total Assets')][j]])) < 0)
                    dict_data[k].append(dlever)
            
                # - change in current ratio.
                elif i == 'dliquid':
                    dliquid = int(((df.loc[(k, 'TCA')][j] / df.loc[(k, 'TCL')][j]) -\
                                   (df.loc[(k-1, 'TCA')][j] / df.loc[(k-1, 'TCL')][j])) > 0)
                    dict_data[k].append(dliquid)
                
                # - total common equity issuance between years.
                elif i == 'eqo':
                    eqo = int(df.loc[(k, 'OSN')][j] < 0)
                    dict_data[k].append(eqo) 
    
                # (3) Operating Efficiency
                # - change in gross margin ratio.
                elif i == 'dgm':
                    dgm = int(((df.loc[(k, 'Gross Profit')][j] / df.loc[(k, 'Total Revenue')][j]) -\
                              (df.loc[(k-1, 'Gross Profit')][j] / df.loc[(k-1, 'Total Revenue')][j])) > 0)
                    dict_data[k].append(dgm)
            
                # - change in asset turnover ratio (revenue/beginning year total assets).
                elif i == 'dturn':
                    dturn = int(((df.loc[(k, 'Total Revenue')][j] / df.loc[(k, 'Total Assets')][j]) -\
                                 (df.loc[(k-1, 'Total Revenue')][j] / df.loc[(k-1, 'Total Assets')][j])) > 0)
                    dict_data[k].append(dturn)
                    
        # updating nested dictionary             
        nested_metric[i] = dict_data
        
    # hierarchical indices and columns
    index = pd.MultiIndex.from_product([[2022, 2021, 2020],   ['EV',
                                                               'WC',
                                                               'TEV',
                                                               'EY',
                                                               'TC',
                                                               'ROIC',
                                                               'ROA',
                                                               'CFO',
                                                               'DROA',
                                                               'Accrual',
                                                               'DLever',
                                                               'DLiquid',
                                                               'EO',
                                                               'DGM',
                                                               'DTurn']],
                                       
                                       
                                   names=['year', ''])
    columns = pd.MultiIndex.from_product([ticker],
                                     names=['ticker'])
    
    # combining metrics from dictionary for each years
    collected_metrics = []
    for x in year:
        for y in nested_metric:
            collected_metrics.append(nested_metric[y][x])

    # mock some data
    data = np.array(collected_metrics)
                     
    # create the DataFrame
    data = pd.DataFrame(data, index=index, columns=columns)
    
    return data


###############################################################################################################################
################################################ MAGIC FORMULA & F-SCORE FUNCTION #############################################


def magic_fscore(df, df1, df2, year):
    
    """ Generate the DataFrame of combination from magic formula to f-score """ 
    
    # create data-frame
    data = pd.DataFrame()
    # add earning yields on the dataframe
    data['Earnings Yield'] = df.T[year]['EY']
    # set tickers as index
    df2 = df2.set_index('Code')
    
    # create empty list for market cap labels
    marketcap = []
    for i in df1.T[year]['Market Cap']:
        if i < 1000000000:
            marketcap.append('Small Cap')
        elif i >= 1000000000 and i <= 10000000000:
            marketcap.append('Mid Cap')
        elif i > 10000000000:
            marketcap.append('Large Cap')
    
    # create empty list for company names
    company = []
    # create empty list for company sectors
    sector  = []         
    for i in list(data.index):
        company.append(df2.loc[i, 'Company'])
        sector.append(df2.loc[i, 'Sector'])
    # add company names
    data['Name'] = company
    # add company sectors
    data['Sector'] = sector
    # add labels of market capitalisation
    data['Market Cap'] = marketcap
    
    # add return on invested capital
    data['ROIC'] = df.T[year]['ROIC']
    # add f-score 
    data['F-Score'] = (df.T[year]['ROA']+df.T[year]['CFO']+df.T[year]['DROA']+\
                       df.T[year]['Accrual']+df.T[year]['DLever']+df.T[year]['DLiquid']+\
                       df.T[year]['EO']+df.T[year]['DGM']+df.T[year]['DTurn']).astype('int64')
    # add magic formula rank
    data['Magic Formula Ranking'] = ((df.T[year]['EY'].rank(ascending=False) +\
               df.T[year]['ROIC'].rank(ascending=False)).rank(method='first')).astype('int64')
    # sorting the values of magic formula 
    data = data.sort_values(by='Magic Formula Ranking')
    # rearranging columns
    data = data[['Name', 'Sector', 'Market Cap', 'Earnings Yield', 'ROIC', 
                 'Magic Formula Ranking', 'F-Score']]
    # reset the index of tickers
    data = data.reset_index()
    
    return data

    
def fscore_magic(df, df1, df2, year):
    
    """ Generate the DataFrame of combination from fscore to magic formula """ 
    
    # create data-frame
    data = pd.DataFrame()
    # add magic formula rank
    data['Magic Formula Ranking'] = ((df.T[year]['EY'].rank(ascending=False) +\
                    df.T[year]['ROIC'].rank(ascending=False)).rank(method='first')).astype('int64')
    # set tickers as index
    df2 = df2.set_index('Code')
    
    # create empty list for market cap labels
    marketcap = []
    for i in df1.T[year]['Market Cap']:
        if i < 1000000000:
            marketcap.append('Small Cap')
        elif i >= 1000000000 and i <= 10000000000:
            marketcap.append('Mid Cap')
        elif i > 10000000000:
            marketcap.append('Large Cap')
    
    # create empty list for company names
    company = []
    # create empty list for company sectors
    sector  = []         
    for i in list(data.index):
        company.append(df2.loc[i, 'Company'])
        sector.append(df2.loc[i, 'Sector'])
    # add company names
    data['Name'] = company
    # add company sectors
    data['Sector'] = sector
    # add labels of market capitalisation
    data['Market Cap'] = marketcap
    # add return on assets
    data['ROA'] = df.T[year]['ROA'].astype('int64')
    # add operating cash flow
    data['CFO'] = df.T[year]['CFO'].astype('int64')
    # add delta return of assets
    data['Delta ROA'] = df.T[year]['DROA'].astype('int64')
    # add accrual
    data['Accrual'] = df.T[year]['Accrual'].astype('int64')
    # add delta leverage
    data['Delta Leverage'] = df.T[year]['DLever'].astype('int64')
    # add delta liquidity
    data['Delta Liquidity'] = df.T[year]['DLiquid'].astype('int64')
    # add equity offering
    data['Equity Offering'] = df.T[year]['EO'].astype('int64')
    # add delta gross margin
    data['Delta Gross Margin'] = df.T[year]['DGM'].astype('int64')
    # add delta turnover
    data['Delta Turnover'] = df.T[year]['DTurn'].astype('int64')
    # add f-score 
    data['F-Score'] = (df.T[year]['ROA']+df.T[year]['CFO']+df.T[year]['DROA']+\
                       df.T[year]['Accrual']+df.T[year]['DLever']+df.T[year]['DLiquid']+\
                       df.T[year]['EO']+df.T[year]['DGM']+df.T[year]['DTurn']).astype('int64')
    # sorting the values of f-score 
    data = data.sort_values(by='F-Score', ascending=False)
    # rearranging columns
    data = data[['Name', 'Sector', 'Market Cap', 'ROA', 'CFO', 'Delta ROA', 'Accrual', 
                 'Delta Leverage', 'Delta Liquidity', 'Equity Offering', 'Delta Gross Margin',
                 'Delta Turnover', 'F-Score', 'Magic Formula Ranking']]
        
    # reset the index of tickers
    data = data.reset_index()
    return data