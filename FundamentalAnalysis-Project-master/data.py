# import libraries
from yahooquery import Ticker
import yahoo_fin.stock_info as yf

def report(data):
    
    # create empty list for balance sheet
    balance_sheet = []
    
    # create empty list for income statement
    income_statement = []
    
    # create empty list for cashflow statement
    cashflow_statement = []
    
    # create empty list for tickers
    tickers = []
    
    
    for i, ticker in zip(list(range(len(data))), data):
        try:
            
            # getting balance sheet data from yahoo finance for the given ticker
            
            # if there is long term debt
            Ticker(ticker+'.JO').balance_sheet(frequency='a').LongTermDebt
            
            balance = Ticker(ticker+'.JO').balance_sheet(frequency='a')
            balance.asOfDate = balance.asOfDate.apply(lambda x: str(x)[:4])
            balance = balance.reset_index(drop=True)
            balance = balance.set_index('asOfDate').T
            # append in the list
            balance_sheet.append(balance[['2022','2021','2020', '2019']])
            
            # getting income statement data from yahoo finance for the given ticker
            
            # if there is gross profit
            Ticker(ticker+'.JO').income_statement(frequency='a').GrossProfit
            
            income = Ticker(ticker+'.JO').income_statement(frequency='a')
            income = income[income.periodType !='TTM']
            income.asOfDate = income.asOfDate.apply(lambda x: str(x)[:4])
            income = income.reset_index(drop=True)
            income = income.set_index('asOfDate').T
            # append in the list
            income_statement.append(income[['2022','2021','2020', '2019']])
            
            # getting cashflow statement data from yahoo finance for the given ticker
            cashflow = yf.get_cash_flow(ticker+'.JO')
            # append in the list
            cashflow_statement.append(cashflow)
        
            # save useful ticker
            tickers.append(ticker)
            
            print(str(i+1)+'. '+'Financial stock data, '+ticker+' ticker is successfully extracted.')
        
        except:
            
            print(str(i+1)+'. '+'Financial stock data, '+ticker+' ticker is not successfully extracted.')

    
    return balance_sheet, income_statement, cashflow_statement, tickers