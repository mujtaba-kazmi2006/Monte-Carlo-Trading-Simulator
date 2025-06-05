📈 Monte Carlo Trading Simulator

A Python-based Monte Carlo simulation to model trade outcomes across various market conditions and instruments (e.g., BTC, ETH, SOL, SPY). This interactive tool helps visualize potential equity curves and assess trading strategy robustness based on win rates, risk-reward ratios, and market scenarios.

🔍 Features

- Simulates **100 trades per game**, with **500 games** by default
- Includes **4 market conditions**:
  - Ideal Setup
  - Bullish Trend
  - Bearish Trend
  - Choppy Market
- Select between different trading **instruments** (BTC, ETH, SOL, SPY)
- Uses **variable win rates** based on market types
- Interactive **Matplotlib GUI** for selecting instruments
- Generates:
  - Multiple equity curves
  - Average performance line
  - Table with trade statistics per market condition

---

📊 Example Output

- Equity curves across simulations with clear trend overlays
- Summary statistics table:
  - Total Trades
  - Wins / Losses
  - Win Rate (%)
  - Net PnL ($)

---



### Requirements
Install dependencies:
pip install numpy matplotlib pandas
