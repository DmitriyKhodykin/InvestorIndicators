"""
The Buffett Indicator is the ratio of total stock market valuation to GDP.

Stock market data from the Yahoo Finance website through `yahoo_fin`:
http://theautomatic.net/yahoo_fin-documentation/#get_analysts_info

Bureau of Economic Analysis USA:
https://apps.bea.gov/API/docs/index.htm
"""
import json
import os

import matplotlib.pyplot as plt
import pandas
import requests
import yahoo_fin.stock_info as si


def main():
    """
    Main workflow.
    """
    make_indicator_graph()


def get_number_of_shares(ticker) -> int:
    """
    Return number of shares outstanding.
    """
    number_of_shares = si.get_quote_data(ticker)['sharesOutstanding']
    return number_of_shares


def get_live_price_of_shares(ticker) -> float:
    """
    Return current share price.
    """
    live_price = si.get_live_price(ticker)
    return live_price


def get_usa_gdp() -> float:
    """
    Get USA GDP from BEA API.
    """
    usa_gdp: float = 0.0
    bea_url = 'https://apps.bea.gov/api/data/'
    bea_api_key = os.environ['BEA_API_KEY']
    bea_method = 'GetData'
    bea_dataset = 'GDPbyIndustry'

    bea_address = f'{bea_url}?&UserID={bea_api_key}&' \
                  f'method={bea_method}&' \
                  f'DataSetName={bea_dataset}&' \
                  f'Year=2020&' \
                  f'Industry=ALL&' \
                  f'tableID=11&' \
                  f'Frequency=A'

    request = requests.get(bea_address)

    try:
        response = json.loads(request.text)  # Text to JSON format
        data = pandas.DataFrame(response['BEAAPI']['Results'][0]['Data'])
        usa_gdp = data['DataValue'].astype(float).sum()
    except (json.JSONDecodeError, KeyError) as error:
        print(error)
    return usa_gdp


def capitalization_calculation(ticker) -> float:
    """
    Calculation of the company's capitalization.
    """
    capitalization = get_number_of_shares(ticker) * get_live_price_of_shares(ticker)
    return capitalization


def capitalization_of_all_issuers():
    """
    Summing up the capitalization's of all companies amount in billions.
    """
    capitalization_of_all: float = 0.0
    tickers = ['msft', 'aapl']
    for ticker in tickers:
        capitalization = capitalization_calculation(ticker)
        capitalization_of_all = round((capitalization_of_all + capitalization) / 1_000_000_000, 2)
    return capitalization_of_all


def buffet_indicator_calculation():
    """
    Calculation of the buffet indicator.
    """
    usa_gdp = get_usa_gdp()
    buffet_indicator = round(capitalization_of_all_issuers() / usa_gdp * 100, 2)
    return buffet_indicator


def make_indicator_graph():
    """
    Make graph from buffet indicator.
    """
    buffet_indicator = buffet_indicator_calculation()
    fig = plt.figure()
    plt.bar(buffet_indicator, height=100)
    plt.xlabel('BuffetIndicator')
    fig.savefig('pics/buffett_indicator.png', dpi=100)


if __name__ == '__main__':
    main()
