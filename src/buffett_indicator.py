"""
The Buffett Indicator is the ratio of total stock market valuation to GDP.
Stock market data from the Yahoo Finance website through `yahoo_fin`
http://theautomatic.net/yahoo_fin-documentation/#get_analysts_info
"""
import matplotlib.pyplot as plt
import pandas
import yahoo_fin.stock_info as si


def main():
    buffett_indicator = BuffettIndicator()
    x = buffett_indicator.capitalization_calculation('msft')
    print(x)


class BuffettIndicator:

    def __init__(self):
        pass

    def get_number_of_shares(self, ticker) -> int:
        """
        Return number of shares outstanding.
        """
        number_of_shares = si.get_quote_data(ticker)['sharesOutstanding']
        return number_of_shares

    def get_live_price_of_shares(self, ticker) -> float:
        """
        Return current share price.
        """
        live_price = si.get_live_price(ticker)
        return live_price

    def capitalization_calculation(self, ticker) -> float:
        """
        Calculation of the company's capitalization.
        """
        capitalization = self.get_number_of_shares(ticker) * self.get_live_price_of_shares(ticker)
        return capitalization

    def capitalization_of_all_issuers(self):
        """
        Summing up the capitalization's of all companies.
        """
        capitalization_of_all: float = 0.0
        tickers = ['msft', 'aapl']
        for ticker in tickers:
            capitalization = self.capitalization_calculation(ticker)
            capitalization_of_all = capitalization_of_all + capitalization
        return capitalization_of_all

    def buffet_indicator_calculation(self):
        pass

    def make_indicator_graph(self):
        pass


if __name__ == '__main__':
    main()
