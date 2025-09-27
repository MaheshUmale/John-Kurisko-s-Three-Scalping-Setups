from tvDatafeed import TvDatafeed, Interval

def fetch_data(symbol: str, exchange: str, interval: Interval, n_bars: int):
    """
    Fetches historical data for a given symbol.

    Args:
        symbol (str): The stock symbol to fetch.
        exchange (str): The exchange where the stock is traded (e.g., 'NASDAQ').
        interval (Interval): The timeframe for the data (e.g., Interval.in_1_minute).
        n_bars (int): The number of historical bars to fetch.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical data, or None if fetching fails.
    """
    try:
        # Using nologin method, which may have limitations
        tv = TvDatafeed()
        data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

if __name__ == '__main__':
    # Example usage: Fetch 1-minute data for AAPL
    print("Fetching 1-minute data for AAPL...")
    aapl_data_1m = fetch_data(symbol='AAPL', exchange='NASDAQ', interval=Interval.in_1_minute, n_bars=1000)
    if aapl_data_1m is not None:
        print("Successfully fetched 1-minute data for AAPL:")
        print(aapl_data_1m.head())

    print("\nFetching 5-minute data for AAPL...")
    aapl_data_5m = fetch_data(symbol='AAPL', exchange='NASDAQ', interval=Interval.in_5_minute, n_bars=1000)
    if aapl_data_5m is not None:
        print("Successfully fetched 5-minute data for AAPL:")
        print(aapl_data_5m.head())