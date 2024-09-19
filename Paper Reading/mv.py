import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# from alpha_vantage.timeseries import TimeSeries
import pypfopt
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import EfficientFrontier

# class MeanVarianceOptimization:
#     def __init__(self, stocks, start_date, end_date):
#         self.stocks = stocks
#         self.start_date = start_date
#         self.end_date = end_date
#         # self.api_key = api_key
#         self.prices = self.get_stock_data()

#     def get_stock_data(self):
#         ts = TimeSeries(key=self.api_key, output_format='pandas')
#         stock_data = pd.DataFrame()

#         for stock in self.stocks:
#             data, _ = ts.get_daily_adjusted(symbol=stock, outputsize='full')
#             data = data['5. adjusted close']
#             data = data.loc[self.start_date:self.end_date]
#             stock_data[stock] = data

#         return stock_data.dropna(how="all")

#     def cov(self):
#         cov = risk_models.CovarianceShrinkage(self.prices).ledoit_wolf()
#         return cov

#     def expected_returns(self):
#         mu = expected_returns.capm_return(self.prices)
#         return mu

#     def weights(self):
#         er = self.expected_returns()
#         cov = self.cov()

#         ef = EfficientFrontier(er, cov, weight_bounds=(None, None))
#         ef.min_volatility()
#         weights = ef.clean_weights()
#         return weights

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pypfopt import risk_models, expected_returns, EfficientFrontier
import os

class MeanVarianceOptimization:
    def __init__(self, stocks, start_date, end_date, data_dir="C:\\Users\\jrnat\\Documents\\GitHub\\dissertation-new\\dissertation\\Paper Reading\\NIFTY50_Stocks\\NIFTY50"):
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.data_dir = data_dir  # Ensure correct directory is being used
        self.prices = self.get_stock_data()

    def get_stock_data(self):
        stock_data = pd.DataFrame()

        for stock in self.stocks:
            # Adjusting file path for "COMPANY.NS.csv" in correct directory
            file_path = os.path.join(self.data_dir, f'{stock}.NS.csv')
            print(f"Looking for file: {file_path}")  # Debugging print to verify file path

            if os.path.exists(file_path):
                data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
                # Use 'Adj Close' for adjusted closing prices
                data = data['Adj Close'].loc[self.start_date:self.end_date]
                stock_data[stock] = data
            else:
                print(f"Data for {stock} not found in {self.data_dir}")

        return stock_data.dropna(how="all")

    def cov(self):
        cov = risk_models.CovarianceShrinkage(self.prices).ledoit_wolf()
        return cov

    def expected_returns(self):
        mu = expected_returns.capm_return(self.prices)
        return mu

    def weights(self):
        er = self.expected_returns()
        cov = self.cov()

        ef = EfficientFrontier(er, cov, weight_bounds=(None, None))
        ef.min_volatility()
        weights = ef.clean_weights()
        return weights

# Example usage
