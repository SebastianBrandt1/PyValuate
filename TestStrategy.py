import pandas as pd
import numpy as np
import pickle


def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv(".\Data\stock_dfs\joined_close_data.csv", index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)
    for i in range(1, hm_days+1):
        df["{}_{}d".format(ticker, i)] = ((df[ticker].shift(-1) - df[ticker]) / df[ticker])

    df.fillna(0, inplace=True)

    # print(df.loc["2000-01-03", "AAPL"])

    return tickers, df


def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0


def extract_featureset(ticker):
    tickers, df = process_data_for_labels(ticker)

    df["{}_target".format(ticker)]

process_data_for_labels("AAPL")
