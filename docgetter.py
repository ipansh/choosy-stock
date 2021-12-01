import pandas as pd
import requests
from base import responsegetter

class docgetter(responsegetter):

    def __init__(self):
        responsegetter.__init__(self)

    def get_income_statement(ticker, period):
        financials_response = responsegetter.get_json_response(ticker,'https://yh-finance.p.rapidapi.com/stock/v2/get-financials',period)
        
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

        return income_statment_df.head(period)