import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("sample_portfolio_returns.csv")

portfolio_returns = df["portfolio_return"]
benchmark_returns = df["SPY"]


df["alpha"] = portfolio_returns-benchmark_returns
df["portfolio_growth"] = (1+portfolio_returns).cumprod()
df["benchmark_growth"] = (1+benchmark_returns).cumprod()
df["cumulative_alpha"] = df["portfolio_growth"] - df["benchmark_growth"]
daily_volatility = 100*(df["portfolio_return"].std())
annualised_volatility = daily_volatility*np.sqrt(252)


print(df.tail(10))
print("")
print(f"Portfolio Daily Volatility: {round(daily_volatility, 2)}%")
print(f"Portfolio Annual Volatility: {round(annualised_volatility, 2)}%")