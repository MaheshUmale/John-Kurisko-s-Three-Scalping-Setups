import pandas as pd
import pandas_ta as ta

def bull_flag_buy_signal(data: pd.DataFrame):
    """
    Identifies the "Bull Flag" buy setup (20-20 Flag).

    Args:
        data (pd.DataFrame): A DataFrame with historical price data (OHLC).

    Returns:
        pd.DataFrame: The input DataFrame with an added 'signal' column.
    """
    if data is None or len(data) < 60:  # Need enough data for indicators
        return None

    # Calculate indicators
    data['ema20'] = ta.ema(data['close'], length=20)

    # Fast Stochastic (9, 3)
    stoch_fast = ta.stoch(high=data['high'], low=data['low'], close=data['close'], k=9, d=3, smooth_k=3)
    data['stoch_fast_d'] = stoch_fast['STOCHd_9_3_3']

    # Slow/Embedded Stochastic (60, 10, 10)
    stoch_slow = ta.stoch(high=data['high'], low=data['low'], close=data['close'], k=60, d=10, smooth_k=10)
    data['stoch_slow_d'] = stoch_slow['STOCHd_60_10_10']

    data['signal'] = 'NONE'

    for i in range(1, len(data)):
        # Condition 1: Embedded Stochastic Check (Slow stoch is holding > 80)
        is_embedded = data['stoch_slow_d'].iloc[i] > 80

        # Condition 2: Price Pullback (Holds on or above the 20 EMA)
        price_holds_ema20 = data['low'].iloc[i] >= data['ema20'].iloc[i]

        # Condition 3: Stochastic Rotation (Fast stoch approaches or touches 20)
        # We'll consider "approaches" as being below a certain threshold, e.g., 25
        fast_stoch_at_20 = data['stoch_fast_d'].iloc[i] <= 25

        if is_embedded and price_holds_ema20 and fast_stoch_at_20:
            # Check if the stochastic is turning up, a common confirmation
            if data['stoch_fast_d'].iloc[i] > data['stoch_fast_d'].iloc[i-1]:
                 data.loc[data.index[i], 'signal'] = 'BUY'

    return data

if __name__ == '__main__':
    print("Bull Flag Strategy module loaded.")
    # Example: Create a dummy dataframe and run the strategy
    dummy_data = pd.DataFrame({
        'open': [100]*100, 'high': [105]*100, 'low': [95]*100, 'close': [102]*100,
    })
    result = bull_flag_buy_signal(dummy_data.copy())
    if result is not None:
        print("Strategy ran on dummy data. Signals found:", (result['signal'] == 'BUY').sum())
    else:
        print("Not enough data for strategy.")