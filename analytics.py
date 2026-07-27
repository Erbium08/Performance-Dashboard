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

def equity_index(returns: pd.Series, initial: float = 1.0) -> pd.Series:
  return initial * (1.0 + returns).cumprod()

def drawdown_series(returns: pd.Series) -> pd.Series:
  return (equity_index(returns) / (equity_index(returns)).cummax() - 1.0)

def max_drawdown(returns: pd.Series) -> float:
  return float(drawdown_series(returns).min())

def annualised_return(returns: pd.Series) -> pd.Series:
  n = len(returns)
  years = n/252
  total_growth = (1.0 + returns).cumprod()

def sharpe_ratio():
  return 0


print(df.tail(10))
print("")
print(f"Portfolio Daily Volatility: {round(daily_volatility, 2)}%")
print(f"Portfolio Annual Volatility: {round(annualised_volatility, 2)}%")