import pandas as pd
import requests
from datetime import datetime

with open('/Users/ilya/Desktop/keys/yahoo_finance.txt','r') as file:
    key = file.readlines()

_KEY_ = key[0]


def get_json_response(ticker, url):

    querystring = {"symbol":ticker,"region":"US"}

    headers = {
                'x-rapidapi-host': "yh-finance.p.rapidapi.com",
                'x-rapidapi-key': _KEY_
                }

    return requests.request("GET", url, headers=headers, params=querystring).json()


def unix_to_date(unix_timestamp):
    ts = int(unix_timestamp)
    return datetime.utcfromtimestamp(ts) #.strftime('%Y-%m-%d')


def get_income_statement(ticker, quarter_periods):
    financials_response = get_json_response(ticker,'https://yh-finance.p.rapidapi.com/stock/v2/get-financials')
        
    income_statment_df = pd.DataFrame()

    for quarter in financials_response['incomeStatementHistoryQuarterly']['incomeStatementHistory']:
        revenue_line = pd.Series([quarter['endDate']['fmt'],
                                  round(quarter['totalRevenue']['raw']/1000000000,3),
                                  round(quarter['grossProfit']['raw']/1000000000,3),
                                  round(quarter['netIncome']['raw']/1000000000,3),
                                  ],
        index = ['quarter','revenue_billion','gross_profit_billion','net_income_billion'])
        income_statment_df = income_statment_df.append(revenue_line, ignore_index=True)

    income_statment_df['quarter'] = [pd.Timestamp(quarter) for quarter in income_statment_df['quarter']]
    income_statment_df['quarter'] = ['4Q2020' if quarter <= pd.Timestamp('2021-01-01T12') else
                                         '1Q2021' if quarter > pd.Timestamp('2021-01-02T12') and quarter < pd.Timestamp('2021-04-01T12') else
                                         '2Q2021' if quarter > pd.Timestamp('2021-04-02T12') and quarter < pd.Timestamp('2021-07-01T12') else
                                         '3Q2021' if quarter > pd.Timestamp('2021-07-02T12') and quarter < pd.Timestamp('2021-10-02T12') else
                                         '4Q2021' for quarter in income_statment_df['quarter']]

    income_statment_df.loc[:,'gross_profit_margin'] = income_statment_df['gross_profit_billion']/income_statment_df['revenue_billion']
    income_statment_df.loc[:,'net_profit_margin'] = income_statment_df['net_income_billion']/income_statment_df['revenue_billion']

    income_statment_df['ticker'] = ticker

    return income_statment_df.head(quarter_periods)


def get_la_ratio(ticker, quarter_periods):

  balance_sheet_response = get_json_response(ticker,'https://yh-finance.p.rapidapi.com/stock/v2/get-balance-sheet')

  balance_df = pd.DataFrame()

  for item in balance_sheet_response['balanceSheetHistoryQuarterly']['balanceSheetStatements']:
    balance_line = pd.Series([item['endDate']['fmt'],
                              item['totalCurrentLiabilities']['raw'],
                              item['totalCurrentAssets']['raw']],
                              index = ['quarter','liabilities','assets'])

    balance_df = balance_df.append(balance_line, ignore_index = True)

  balance_df.loc[:,'la_ratio'] = round(balance_df['liabilities']/balance_df['assets'],2)
  balance_df.loc[:,'assets_billion'] = round(balance_df['assets']/1000000000,2)
  balance_df.loc[:,'liabilities_billion'] = round(balance_df['liabilities']/1000000000,2)
  balance_df = balance_df.drop(columns = ['assets','liabilities'])
  balance_df['ticker'] = ticker

  return balance_df.head(quarter_periods)

def get_pe_ratio(ticker, quarter_periods):

    stats_response = get_json_response(ticker, "https://yh-finance.p.rapidapi.com/stock/v2/get-statistics")

    ratio_df = pd.DataFrame()

    if stats_response['timeSeries']['quarterlyPeRatio'] != []:
        for quarter in stats_response['timeSeries']['quarterlyPeRatio']:
            if quarter is not None:
                pd_row = pd.Series([quarter['asOfDate'], quarter['reportedValue']['fmt']],
                index = ['quarter','pe_ratio'])
                ratio_df = ratio_df.append(pd_row, ignore_index=True)

    if ratio_df.empty == True:
        ratio_df['ticker'] = [ticker]
        ratio_df['pe_ratio'] = [None]
        ratio_df['quarter'] = [datetime.now().date()]

    else:
        pass

    ratio_df['ticker'] = ticker

    return ratio_df.sort_values(by = 'quarter', ascending = False).head(quarter_periods)

def get_weekly_history_df(ticker):

    history_response = get_json_response(ticker, "https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data")

    weekly_history_df = pd.DataFrame(history_response['prices'])[['date','close']]
    weekly_history_df.loc[:,'date'] = weekly_history_df['date'].apply(lambda x: unix_to_date(x))

    weekly_history_df.loc[:,'week'] = [pd.Timestamp(date).week for date in weekly_history_df['date']]
    weekly_history_df.loc[:,'year'] = [pd.Timestamp(date).year for date in weekly_history_df['date']]

    weekly_history_df.loc[:,'close'] = weekly_history_df['close'].round(1)

    return weekly_history_df[['date','year','week','close']]

def list_perfomance(ticker):
    weekly_history_df = get_weekly_history_df(ticker)

    attributes = ['ticker','yoy_growth','std','mean_price','volatility','last_close_price']

    performance_list = [ticker,\
                        round((weekly_history_df.iloc[0]['close'] - weekly_history_df.iloc[-1]['close'])/weekly_history_df.loc[0]['close'],3),\
                        round(weekly_history_df['close'].std(),2),
                        round(weekly_history_df['close'].mean(),2),
                        round(weekly_history_df['close'].std()/weekly_history_df['close'].mean(),2),
                        round(weekly_history_df.iloc[0]['close'],1)
                        ]

    performance_row = pd.Series(performance_list, index = attributes)

    return performance_row

def get_stock_weekly_changes(ticker, last_weeks):
    history_json_response = get_json_response(ticker,'https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data')

    history_df = pd.DataFrame(history_json_response['prices'])

    history_df.loc[:,'date'] = [unix_to_date(date) for date in history_df['date']]

    history_df.loc[:,'year'] = [date.isocalendar()[0] for date in history_df['date']]
    history_df.loc[:,'week'] = [date.isocalendar()[1] for date in history_df['date']]

    weekly_history_df = history_df[['year','week','close']].groupby(['year','week']).mean()
    weekly_history_df = weekly_history_df.reset_index()

    weekly_history_df['previous_week_close'] = weekly_history_df['close'].shift(1)

    weekly_history_df['wow_change_%'] = [round((close-previous_close)/previous_close,3)*100 if previous_close is not None else 0
                                     for close, previous_close in zip(weekly_history_df['close'],
                                                                  weekly_history_df['previous_week_close'])]

    weekly_history_df['year-week'] = weekly_history_df['year'].astype('str')+'~'+weekly_history_df['week'].astype('str')

    weekly_history_df = weekly_history_df.rename(columns = {'wow_change_%': ticker.lower()})

    return weekly_history_df.tail(last_weeks)[['year-week',ticker.lower()]]

def get_stock_daily_price(ticker, day_periods):
    history_json_response = get_json_response(ticker,'https://yh-finance.p.rapidapi.com/stock/v3/get-historical-data')

    history_df = pd.DataFrame(history_json_response['prices'])

    history_df.loc[:,'date'] = [unix_to_date(date).date() for date in history_df['date']]

    history_df = history_df[['date','close']].head(day_periods)

    history_df = history_df.rename(columns = {'close': ticker.lower()})

    return history_df