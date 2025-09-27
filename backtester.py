import pandas as pd

def run_backtest(data, signals_df, sl_pct=0.01, tp_pct=0.02):
    """
    Runs a simple backtest on a given dataset with signals.

    Args:
        data (pd.DataFrame): DataFrame with OHLC data.
        signals_df (pd.DataFrame): DataFrame with a 'signal' column ('BUY', 'SELL', 'NONE').
        sl_pct (float): Stop-loss percentage.
        tp_pct (float): Take-profit percentage.

    Returns:
        pd.DataFrame: A DataFrame containing the record of all trades.
    """
    trades = []
    position = None
    entry_price = 0

    if 'signal' not in signals_df.columns:
        print("Error: 'signal' column not found in signals DataFrame.")
        return pd.DataFrame()

    for i in range(len(data)):
        # --- Handle Exits ---
        if position:
            current_price = data['close'].iloc[i]
            if position == 'LONG':
                if current_price <= entry_price * (1 - sl_pct) or current_price >= entry_price * (1 + tp_pct):
                    reason = 'SL' if current_price <= entry_price * (1 - sl_pct) else 'TP'
                    trades[-1].update({
                        'exit_date': data.index[i],
                        'exit_price': current_price,
                        'exit_reason': reason,
                        'pnl': (current_price - entry_price) / entry_price
                    })
                    position = None
            elif position == 'SHORT':
                if current_price >= entry_price * (1 + sl_pct) or current_price <= entry_price * (1 - tp_pct):
                    reason = 'SL' if current_price >= entry_price * (1 + sl_pct) else 'TP'
                    trades[-1].update({
                        'exit_date': data.index[i],
                        'exit_price': current_price,
                        'exit_reason': reason,
                        'pnl': (entry_price - current_price) / entry_price
                    })
                    position = None

        # --- Handle Entries ---
        if not position:
            signal = signals_df['signal'].iloc[i]
            if signal == 'BUY':
                position = 'LONG'
                entry_price = data['close'].iloc[i]
                trades.append({
                    'entry_date': data.index[i],
                    'entry_price': entry_price,
                    'side': 'LONG'
                })
            elif signal == 'SELL':
                position = 'SHORT'
                position = 'SHORT'
                entry_price = data['close'].iloc[i]
                trades.append({
                    'entry_date': data.index[i],
                    'entry_price': entry_price,
                    'side': 'SHORT'
                })

    return pd.DataFrame(trades)

def calculate_metrics(trades_df):
    """
    Calculates performance metrics from a DataFrame of trades.

    Args:
        trades_df (pd.DataFrame): The DataFrame of trades from the backtest.

    Returns:
        dict: A dictionary of performance metrics.
    """
    if trades_df.empty or 'pnl' not in trades_df.columns or trades_df['pnl'].isnull().all():
        return {
            "Total Trades": 0,
            "Win Rate (%)": 0,
            "Total PnL (%)": 0,
            "Max Drawdown (%)": 0,
        }

    # Ensure PnL is numeric
    trades_df['pnl'] = pd.to_numeric(trades_df['pnl'], errors='coerce').fillna(0)

    # Win Rate
    winning_trades = trades_df[trades_df['pnl'] > 0]
    win_rate = len(winning_trades) / len(trades_df) * 100 if len(trades_df) > 0 else 0

    # Total PnL
    total_pnl = trades_df['pnl'].sum()

    # Drawdown
    cumulative_pnl = (1 + trades_df['pnl']).cumprod()
    peak = cumulative_pnl.expanding(min_periods=1).max()
    drawdown = (cumulative_pnl / peak) - 1
    max_drawdown = drawdown.min() if not drawdown.empty else 0

    return {
        "Total Trades": len(trades_df),
        "Win Rate (%)": f"{win_rate:.2f}",
        "Total PnL (%)": f"{total_pnl * 100:.2f}",
        "Max Drawdown (%)": f"{max_drawdown * 100:.2f}",
    }

if __name__ == '__main__':
    print("Backtester module loaded.")