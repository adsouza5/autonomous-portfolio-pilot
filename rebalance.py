#!/usr/bin/env python3
import json
import os
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
from dotenv import load_dotenv
from openai import OpenAI

# Configuration
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Data Fetching
def fetch_current_prices(symbols):
    data = yf.download(
        tickers=" ".join(symbols),
        period="1d", interval="1m", progress=False
    )
    if isinstance(data.columns, pd.MultiIndex):
        latest = data['Close'].iloc[-1]
        return { sym: float(latest[sym]) for sym in symbols }
    else:
        return { symbols[0]: float(data['Close'].iloc[-1]) }

def fetch_historical(symbol, days=30):
    hist = yf.Ticker(symbol).history(period=f"{days}d")
    return hist['Close']

# Optimization

def compute_optimal_weights(historical_prices, risk_aversion=0.5):
    returns = historical_prices.pct_change().dropna()
    mu = returns.mean()
    Sigma = returns.cov().values
    n = len(mu)

    def objective(w):
        return -mu.dot(w) + risk_aversion * w.T.dot(Sigma).dot(w)

    cons = [{"type":"eq", "fun": lambda w: w.sum() - 1}]
    bounds = [(0,1)] * n
    w0 = np.ones(n)/n

    res = minimize(objective, w0, bounds=bounds, constraints=cons)
    return dict(zip(historical_prices.columns, res.x))

# Main Loop
if __name__ == "__main__":
    # Load portfolio
    with open("portfolio.json") as f:
        portfolio = json.load(f)
    symbols = list(portfolio.keys())

    # Fetch data
    print("Fetching current prices…")
    current_prices = fetch_current_prices(symbols)
    print("Fetching historical data…")
    hist = pd.concat(
        [fetch_historical(s) for s in symbols],
        axis=1, keys=symbols
    )

    # Compute weights
    target_weights = compute_optimal_weights(hist, risk_aversion=0.5)
    total_value = sum(current_prices[s]*portfolio[s] for s in symbols)
    current_weights = {
        s: (current_prices[s]*portfolio[s]) / total_value
        for s in symbols
    }

    # Dry-run orders
    trades = []
    print("\nProposed orders (dry run):")
    for s in symbols:
        delta_w = target_weights[s] - current_weights[s]
        shares = round(delta_w * total_value / current_prices[s])
        if shares > 0:
            line = f"BUY  {shares} shares of {s}"
        elif shares < 0:
            line = f"SELL {abs(shares)} shares of {s}"
        else:
            continue
        trades.append(line)
        print(line)

    if not trades:
        print("  (No trades needed.)")

    # LLM Explanation 
    prompt = (
        f"I have a portfolio: {portfolio}\n"
        f"Current prices: {current_prices}\n"
        f"I ran a mean-variance optimization (λ=0.5) and generated these trades:\n"
        + "\n".join(trades) +
        "\n\nIn two sentences, explain why this rebalance makes sense."
    )

    resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"system","content":"You are a helpful financial assistant."},
            {"role":"user","content":prompt} ],
    max_tokens=100
)

    explanation = resp.choices[0].message.content.strip()

    print("\nLLM Explanation:")
    print(explanation)
    print("\nDone.")
