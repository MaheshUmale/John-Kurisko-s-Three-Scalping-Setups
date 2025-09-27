import pandas as pd
from tvDatafeed import Interval

from data_fetcher import fetch_data
from backtester import run_backtest, calculate_metrics
from strategies.holy_grail import holy_grail_buy_signal
from strategies.bull_flag import bull_flag_buy_signal
from strategies.bear_flag import bear_flag_short_signal

def run():
    """
    Main execution function to run the backtesting process.
    """
    symbols_to_test = [
        {'symbol': 'AAPL', 'exchange': 'NASDAQ'},
        # Add more symbols here if needed
        # {'symbol': 'GOOGL', 'exchange': 'NASDAQ'},
    ]

    strategies = {
        "Holy Grail (1m)": (holy_grail_buy_signal, Interval.in_1_minute),
        "Bull Flag (5m)": (bull_flag_buy_signal, Interval.in_5_minute),
        "Bear Flag (5m)": (bear_flag_short_signal, Interval.in_5_minute),
    }

    results_summary = []

    for config in symbols_to_test:
        symbol = config['symbol']
        exchange = config['exchange']
        print(f"--- Processing Symbol: {symbol} ---")

        for name, (strategy_func, interval) in strategies.items():
            print(f"Running strategy: {name}...")

            # 1. Fetch Data
            data = fetch_data(symbol=symbol, exchange=exchange, interval=interval, n_bars=5000)
            if data is None or data.empty:
                print(f"Could not fetch data for {symbol} on {interval}. Skipping.")
                continue

            # 2. Generate Signals
            signals_df = strategy_func(data.copy())
            if signals_df is None:
                print(f"Not enough data to generate signals for {name}. Skipping.")
                continue

            # 3. Run Backtest
            # Using 1% SL and 2% TP as defined in the backtester
            trades_df = run_backtest(data, signals_df, sl_pct=0.01, tp_pct=0.02)

            # 4. Calculate Metrics
            metrics = calculate_metrics(trades_df)

            results_summary.append({
                "Symbol": symbol,
                "Strategy": name,
                **metrics
            })
            print(f"Strategy {name} for {symbol} processed.")

    # 5. Generate TESTRESULTS.md
    results_df = pd.DataFrame(results_summary)
    with open("TESTRESULTS.md", "w") as f:
        f.write("# Trading Strategy Backtest Results\n\n")
        f.write(results_df.to_markdown(index=False))
        f.write("\n")

    print("\n--- Backtesting Complete ---")
    print("Results saved to TESTRESULTS.md")
    print(results_df)


if __name__ == "__main__":
    run()