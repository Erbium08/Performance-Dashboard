import pandas as pd
import numpy as np
import matplotlib
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


print(df.tail(10))
print("")
print(f"Portfolio Daily Volatility: {round(daily_volatility, 2)}%")
print(f"Portfolio Annual Volatility: {round(annualised_volatility, 2)}%")

# 1. Dynamic Bins (-3.0 to +3.0 by 0.5)
v = np.arange(-3.0, 3.5, 0.5)
labels = [f"<{v[0]:.1f}"] + [f"{a:.1f}" for a in v[:-1]] + [f">{v[-1]:.1f}"]
counts = (
    pd.cut(
        portfolio_returns * 100,
        bins=np.r_[-np.inf, v, np.inf],
        labels=labels,
    )
    .value_counts()
    .sort_index()
)

# 2. Standard Matplotlib Styling (Classic Blue & Orange accents)
colors = np.where(np.arange(len(counts)) < 7, "#1f77b4", "#ff7f0e")

fig, ax = plt.subplots(figsize=(8, 4), dpi=120)
bars = ax.bar(
    counts.index,
    counts,
    color=colors,
    edgecolor="black",
    linewidth=0.8,
    width=0.8,
)
ax.bar_label(bars, padding=2, fontsize=7)

# 3. Classic Annotations & Grid
loss, win = (portfolio_returns < 0).sum(), (portfolio_returns > 0).sum()
ax.set(
    title=f"Daily Returns Distribution (%)\nLosing: {loss:,} | Winning: {win:,}",
    xlabel="Daily trading net returns (%)",
)
ax.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.7)
ax.set_axisbelow(True)
ax.tick_params(axis="x", labelrotation=45, labelsize=7)

plt.tight_layout()
plt.show()