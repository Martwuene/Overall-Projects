# import the required libraries 
import streamlit as st
from yahooquery import Ticker
import yahoo_fin.stock_info as yf
import pandas as pd
import numpy as np
import time
from information import magic_fscore
from information import fscore_magic
from information import financial_indicators
import information


# set page configuration
st.set_page_config(page_title="Quant Webpage")

# set a title
st.title("Fundamental Analysis | JSE Stocks")

# display line
st.write("-----")

# Set a two column diplay
col1, col2 = st.columns(2,gap="large")

# Write on first column
with col1:
    st.write("__Market Capitalization__")
    text = r'''
                - Small Cap $< R1 B$
                - $R1 B \leq$ Medium Cap $\leq R10 B$
                - Large Cap $> R10 B$ 
            '''
    st.write(text)
    st.write('')
    st.caption('> B = Billion of ZAR (i.e., South African Rand)')

# Write on second column
with col2:
    st.write("__Ensemble Strategies__")
    st.markdown(
        """
            - Magic Formula
            - F-Score
        """
    )

# Add line
st.write('----')
# Add subhead
st.write('##### Data Upload')
# Set data upload
uploaded_file = st.file_uploader("Choose an Excel file")
if uploaded_file is None:
    st.write('')

if uploaded_file is not None:

    # can be used wherever a "file-like" object is accepted:
    data = pd.read_excel('JSE Total Companies List_rev1.xlsx', usecols=['Code', 'Company', 'Sector'],header=1)
    
    # filtering data to tickers
    stock_tickers = data.Code

    st.write('')
    st.write('')
    # data status
    st.write('##### Status')

    # data extraction reporting
    # create empty list for balance sheet
    balance_sheet = []
    
    # create empty list for income statement
    income_statement = []

    # create empty list for cashflow statement
    cashflow_statement = []
    
    # create empty list for tickers
    tickers = []

    latest_iteration = st.empty()
    bar = st.progress(0) 
    for i, ticker in zip(list(range(len(stock_tickers))), stock_tickers):
        try:
            
            # getting balance sheet data from yahoo finance for the given ticker
            
            # if there is long term debt
            ltd = Ticker(ticker+'.JO').balance_sheet(frequency='a').LongTermDebt
            
            balance = Ticker(ticker+'.JO').balance_sheet(frequency='a')
            balance.asOfDate = balance.asOfDate.apply(lambda x: str(x)[:4])
            balance = balance.reset_index(drop=True)
            balance = balance.set_index('asOfDate').T
            # append in the list
            balance_sheet.append(balance[['2022','2021','2020','2019']])
            
            # getting income statement data from yahoo finance for the given ticker

            # if there is gross profit
            gp = Ticker(ticker+'.JO').income_statement(frequency='a').GrossProfit

            income = Ticker(ticker+'.JO').income_statement(frequency='a')
            income = income[income.periodType !='TTM']
            income.asOfDate = income.asOfDate.apply(lambda x: str(x)[:4])
            income = income.reset_index(drop=True)
            income = income.set_index('asOfDate').T
            # append in the list
            income_statement.append(income[['2022','2021','2020','2019']])
            
            # getting cashflow statement data from yahoo finance for the given ticker
            cashflow = yf.get_cash_flow(ticker+'.JO')
            # append in the list
            cashflow_statement.append(cashflow)

            # save useful ticker
            tickers.append(ticker)

        except:
                print('')

        # status of data uploading progress
        latest_iteration.text(f'Total stock: {(i+1)} ({((i+1)/len(stock_tickers))*100}%)')
        time.sleep(0.1)
        bar.progress(int((100/len(stock_tickers))*(i+1)))

    # displaying required financial indicators
    financial_data = financial_indicators(balance_sheet, income_statement, cashflow_statement,
                                          ticker=tickers)

    # filling NaN values with zeros
    financial_data = financial_data.fillna(0)

    # displaying required financial metric
    financial_metrics = information.financial_metrics(df=financial_data, ticker=tickers)

    # displaying stocks that are listed by magic formula to f-score
    mf1 = magic_fscore(financial_metrics, financial_data, data, 2022)
    mf2 = magic_fscore(financial_metrics, financial_data, data, 2021)
    mf3 = magic_fscore(financial_metrics, financial_data, data, 2020)

    # displaying stocks that are listed by f-score to magic formula
    fm1 = fscore_magic(financial_metrics, financial_data, data, 2022)
    fm2 = fscore_magic(financial_metrics, financial_data, data, 2021)
    fm3 = fscore_magic(financial_metrics, financial_data, data, 2020)

    # Display status
    st.caption(f'> Successfully extracted financial stock data:  {len(tickers)}')
    st.caption(f'> Unsuccessfully extracted financial stock data:  {len(stock_tickers)-len(tickers)}')

    # Add line
    st.write('----')
   
    # Creating spaces
    st.write(' ')
    st.write(' ')

    # Add subhead
    st.write('##### Magic Formula | F-Score')

    # Set two tabs
    tab1, tab2, tab3 = st.tabs(["2022", "2021", "2020"])
    # displaying stocks that are listed by magic formula & f-score
    tab1.table(mf1.head(30))
    tab2.table(mf2.head(30))
    tab3.table(mf3.head(30))

    # Creating spaces
    st.write(' ')
    st.write(' ')
    st.write(' ')

    # Add subhead
    st.write('##### F-Score | Magic Formula')

    # Set two tabs
    tab1, tab2, tab3 = st.tabs(["2022", "2021", "2020"])
    # displaying stocks that are listed by magic formula & f-score
    tab1.table(fm1.head(30))
    tab2.table(fm2.head(30))
    tab3.table(fm3.head(30))

    # Creating spaces
    st.write(' ')
    st.write(' ')
    st.write(' ')

    st.write('##### Glossary')

    # Create dictionary for glossary
    glossary = {'Term':['Accrual', 'Cash flow from operating (CFO)', '∆ gross margin', '∆ leverage',
                '∆ liquidity', '∆ return on assets', '∆ turnover', 'Earnings yield','Equity offering', 
                "Greenblatt's magic formula", 'Market capitalisation', 'Name', 'Piotroski F-Score', 
                'Return on assets (ROA)', 'Return on invested capital (ROIC)', 'Sector', 'Ticker'], 
             
    'Definition':['An accounting method in which payments and expenses are credited and debited when earned or incurred.\
                   CFO compared to ROA. If CFO > ROA, F score is 1. Otherwise, F score is 0.',

                  'Indicates whether or not a company has enough funds coming in to pay its bills or operating expenses.\
                   Operating cash flow divided by year beginning total assets. F score is 1 if CFO is positive, 0 otherwise.',

                  "Change in gross margin ratio. If the current year's ratio minus prior year's ratio > 0, F Score is 1,\
                   0 otherwise.",

                  'Change in long-term debt/average total assets ratio. If the ratio compared to the prior year is lower,\
                   F score is 1, 0 otherwise.',

                  'Change in current ratio. If the current ratio increases from the prior year, F score is 1, 0 otherwise.',

                  'Change in ROA from the prior year. If ∆ROA > 0, F score is 1. Otherwise, F score is 0.',

                  "Change in asset turnover ratio (revenue/beginning year total assets). If current year's ratio minus prior\
                   years > 0, F score is 1, 0 otherwise.",

                  'The earnings per share for the most recent 12-month period divided by the current market price per share.',

                  'Total common equity between years. If common equity increases compared to prior year, F score is 1, 0 otherwise.',

                  'A simple, rules-based system designed to bring high returns within reach of the average investor by measuring\
                    the strength of a company',

                  "The total value of a publicly traded company's outstanding common shares owned by stockholders.",

                  'The name of the companies',

                  "A number between 0 and 9 which is used to assess strength of company's financial position.",

                  'Net Income divided by year beginning total assets. F score is 1 if ROA is positive, 0 otherwise.',

                  'The amount of money a company makes that is above the average cost it pays for its debt and equity\
                     capital.',

                  'An area of the economy in which businesses share the same or related business activity, product,\
                         or service. ',
                  
                  'An abbreviation used to uniquely identify publicly traded shares of a particular stock on a particular\
                     stock market.']}

    # Set to be on table
    st.table(glossary)