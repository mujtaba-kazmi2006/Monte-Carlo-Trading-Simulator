import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import random
import pandas as pd

# === GAME SETTINGS ===
starting_balance = 1000
risk_per_trade = 1
reward_to_risk = 2.0
base_win_rate = 0.55
trades_in_one_game = 100
number_of_games = 500

# === Market Situations ===
market_conditions = ["ideal setup", "bullish trend", "bearish trend", "choppy"]

# === Instruments ===
instruments = {
    "1": {"name": "BTC/USDT"},
    "2": {"name": "ETH/USDT"},
    "3": {"name": "SOL/USDT"},
    "4": {"name": "SPY"},
}
selected_instrument_key = "1"

# === SIMULATION FUNCTION ===
def run_simulation(instrument_key):
    market_stats = {cond: {'trades': 0, 'wins': 0, 'losses': 0, 'pnl': 0} for cond in market_conditions}
    all_games = []

    def market_situation():
        return random.choice(market_conditions)

    for game in range(number_of_games):
        balance = starting_balance
        equity_curve = [balance]

        for _ in range(trades_in_one_game):
            market = market_situation()
            market_stats[market]['trades'] += 1

            if market == "ideal setup":
                win_chance = base_win_rate + 0.10
            elif market == "bullish trend":
                win_chance = base_win_rate + 0.05
            elif market == "bearish trend":
                win_chance = base_win_rate - 0.05
            elif market == "choppy":
                win_chance = base_win_rate - 0.10
            else:
                win_chance = base_win_rate

            win = np.random.rand() < win_chance

            if win:
                profit = risk_per_trade * reward_to_risk
                balance += profit
                market_stats[market]['wins'] += 1
                market_stats[market]['pnl'] += profit
            else:
                loss = risk_per_trade
                balance -= loss
                market_stats[market]['losses'] += 1
                market_stats[market]['pnl'] -= loss

            equity_curve.append(balance)

        all_games.append(equity_curve)

    return all_games, market_stats


# === PLOTTING FUNCTION ===
def plot_results(equity_curves, market_stats, instrument_name):
    df = pd.DataFrame([{
        'Market Type': mkt,
        'Total Trades': stats['trades'],
        'Wins': stats['wins'],
        'Losses': stats['losses'],
        'Win Rate (%)': round(stats['wins'] / stats['trades'] * 100, 2) if stats['trades'] > 0 else 0,
        'PnL ($)': round(stats['pnl'], 2)
    } for mkt, stats in market_stats.items()])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [4, 1]}, facecolor="#111")

    # Plot equity curves
    ax1.set_facecolor("#111")
    for curve in equity_curves:
        ax1.plot(curve, color='skyblue', alpha=0.05)

    avg_curve = np.mean(equity_curves, axis=0)
    ax1.plot(avg_curve, color='lime', label='Average Equity', linewidth=2)

    ax1.set_title(f"Monte Carlo Simulation By Mujtaba Kazmi- {instrument_name}", color='white')
    ax1.set_xlabel("Number of Trades", color='white')
    ax1.set_ylabel("Balance ($)", color='white')
    ax1.tick_params(colors='white')
    ax1.grid(True, alpha=0.2)
    ax1.legend()

    # Plot table
    ax2.axis('off')
    table = ax2.table(
        cellText=df.values.tolist(),
        colLabels=df.columns.tolist(),
        cellLoc='center',
        loc='center'
    )
    table.scale(1, 2)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Color table
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#444')
        if row == 0:
            cell.set_facecolor('#222')
            cell.get_text().set_color('white')
            cell.get_text().set_weight('bold')
        else:
            cell.set_facecolor('#333')
            cell.get_text().set_color('white')

    plt.tight_layout()
    plt.show()


# === CALLBACK ON RADIO SELECTION ===
def on_select(label):
    global selected_instrument_key
    for key, info in instruments.items():
        if info["name"] == label:
            selected_instrument_key = key
            break
    instrument = instruments[selected_instrument_key]["name"]
    curves, stats = run_simulation(selected_instrument_key)
    plot_results(curves, stats, instrument)


# === UI SELECTION PANEL ===
fig, ax = plt.subplots(figsize=(6, 4))
plt.subplots_adjust(left=0.3)
ax.set_title("Select Instrument to Simulate", fontsize=14)
ax.axis('off')

radio_labels = [i["name"] for i in instruments.values()]
radio_ax = plt.axes([0.05, 0.4, 0.2, 0.4], facecolor='#222')
radio = RadioButtons(radio_ax, radio_labels)

# Set label styles
for label in radio.labels:
    label.set_color('white')
    label.set_fontsize(10)

radio.on_clicked(on_select)
plt.show()

