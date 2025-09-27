import pandas as pd
import pandas_ta as ta

def holy_grail_buy_signal(data: pd.DataFrame):
    """
    Identifies the "Holy Grail" buy setup based on Quad Divergence.

    Args:
        data (pd.DataFrame): A DataFrame with historical price data (OHLC).

    Returns:
        pd.DataFrame: The input DataFrame with an added 'signal' column.
    """
    if data is None or len(data) < 60:  # Need enough data for the slowest stochastic
        return None

    # Calculate the four stochastic oscillators using pandas-ta
    # The README specifies (k, d) for fast/medium and (k, d, smooth_d) for slow.
    # pandas-ta stoch is (k, d, smooth_k). We will use the 'd' line as specified.
    # Fast Stochastic (9, 3)
    stoch_fast = ta.stoch(high=data['high'], low=data['low'], close=data['close'], k=9, d=3, smooth_k=3)
    data['stoch_fast_d'] = stoch_fast['STOCHd_9_3_3']

    # Medium Stoch 1 (14, 3)
    stoch_medium1 = ta.stoch(high=data['high'], low=data['low'], close=data['close'], k=14, d=3, smooth_k=3)
    data['stoch_medium1_d'] = stoch_medium1['STOCHd_14_3_3']

    # Medium Stoch 2 (40, 4)
    stoch_medium2 = ta.stoch(high=data['high'], low=data['low'], close=data['close'], k=40, d=4, smooth_k=4)
    data['stoch_medium2_d'] = stoch_medium2['STOCHd_40_4_4']

    # Slow/Embedded Stoch (60, 10, 10)
    stoch_slow = ta.stoch(high=data['high'], low=data['low'], close=data['close'], k=60, d=10, smooth_k=10)
    data['stoch_slow_d'] = stoch_slow['STOCHd_60_10_10']

    data['signal'] = 'NONE'

    # This is a simplified loop to find the pattern. A more robust implementation
    # would use state machines or more complex vectorized operations.
    for i in range(1, len(data)):
        # Step 1: Quad Rotation Trigger (L1)
        # Check if all stochastics were below 20 on the previous bar
        all_stochs_below_20_prev = (
            data['stoch_fast_d'].iloc[i-1] < 20 and
            data['stoch_medium1_d'].iloc[i-1] < 20 and
            data['stoch_medium2_d'].iloc[i-1] < 20 and
            data['stoch_slow_d'].iloc[i-1] < 20
        )

        if all_stochs_below_20_prev:
            l1_price = data['low'].iloc[i-1]
            l1_stoch_fast = data['stoch_fast_d'].iloc[i-1]

            # Look ahead for the rest of the pattern
            for j in range(i, len(data)):
                # Step 2: Initial Bounce (Fast stoch goes above 20)
                if data['stoch_fast_d'].iloc[j] > 20:
                    # Step 3: Price Retest (L2)
                    # Look for a new low after the bounce
                    for k in range(j + 1, len(data)):
                        if data['low'].iloc[k] <= l1_price:
                            l2_price = data['low'].iloc[k]
                            l2_stoch_fast = data['stoch_fast_d'].iloc[k]

                            # Step 4: Divergence Confirmation
                            # At L2, fast stoch has a HIGHER low than at L1
                            # AND it turns back up above 20
                            stoch_divergence = l2_stoch_fast > l1_stoch_fast

                            if stoch_divergence:
                                # Check if stoch turns up above 20 after L2
                                for m in range(k + 1, len(data)):
                                    if data['stoch_fast_d'].iloc[m] > 20:
                                        # Step 5: Entry Signal
                                        data.loc[data.index[m], 'signal'] = 'BUY'
                                        # Found a signal, break inner loops to avoid re-evaluating this segment
                                        i = m + 1
                                        break
                                # Break from L2 search
                                break
                    # Break from bounce search
                    break
    return data

if __name__ == '__main__':
    # This is a placeholder for testing. We will use the main script for actual runs.
    print("Holy Grail Strategy module loaded.")
    # Example: Create a dummy dataframe and run the strategy
    dummy_data = pd.DataFrame({
        'open': [100]*100, 'high': [105]*100, 'low': [95]*100, 'close': [102]*100,
    })
    # This will likely not produce a signal with dummy data, but it tests the structure.
    result = holy_grail_buy_signal(dummy_data.copy())
    if result is not None:
        print("Strategy ran on dummy data. Signals found:", (result['signal'] == 'BUY').sum())
    else:
        print("Not enough data for strategy.")