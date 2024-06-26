from mftool import Mftool
import numpy as np
import pandas as pd
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
import requests
from bs4 import BeautifulSoup

def current_bond_yield():
    url = "https://www.worldgovernmentbonds.com/bond-historical-data/india/10-years/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the yield value
    yield_element = soup.find("div",{"class":"w3-cell"}).get_text()
    bond_yield = float(yield_element.strip()[:-1])/100
    return bond_yield

def calculate_optimal_weights(bond_yield,tickers=None):
    MF = Mftool()
    # Fetch data
    if tickers is None:
        tickers = ["120505","118481","130503","120586","120251","127042","118778","120828","152067"]
    df = pd.DataFrame()
    for code in tickers:
        df[code] = MF.get_scheme_historical_nav(code,as_Dataframe=True)['nav']
    df = df.dropna()
    s = df.select_dtypes(include='object').columns
    df[s] = df[s].astype("float")
    df = df.iloc[::-1]

    daily_returns = df.pct_change().dropna()
    period = len(daily_returns)
    daily_returns = daily_returns[period-20*2:period]

    mu = mean_historical_return(df[period-20*2:period])
    S = CovarianceShrinkage(df[period-20*2:period]).ledoit_wolf(shrinkage_target='single_factor')

    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe(risk_free_rate=bond_yield)

    cleaned_weights = ef.clean_weights()
    
    return cleaned_weights

def ticker_to_name(tickers=None):
    MF = Mftool()
    if tickers is None:
        tickers = ["120505","118481","130503","120586","120251","127042","118778","120828","152067"]

    names = []
    
    for code in tickers:
        names.append(MF.get_scheme_quote(code)['scheme_name'])
    return names
