import yfinance as yf

class CheckMyStockVitals:

    def __init__(self):

        """ Base class with a couple of functions that return basic info.
        """

    def check_vitals(company_name):
        stock_ticker = yf.Ticker(company_name)
        stock_info = stock_ticker.info
        price = stock_info['regularMarketOpen']
        name = stock_info['shortName']
        print("The Market Open Price today for {} is ${}.".format(name, price))

class VisualizeMyStock(CheckMyStockVitals):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.
    """

    def __init__(self):

        CheckMyStockVitals.__init__(self)