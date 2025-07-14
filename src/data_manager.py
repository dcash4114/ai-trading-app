from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import os
import logging
import keyring

class DataManager:
    def __init__(self):
        self.tv = None
        self.live = None

    def login(self, username, password):
        try:
            self.tv = TvDatafeed(username, password=password)
            self.live = self.tv
            return True
        except Exception as e:
            logging.error(f"Login error: {e}")
            return False

    def get_historical_data(self, symbol, exchange, interval, n_bars=5000):
        if self.tv is None:
            raise ValueError("Not logged in to TradingView. Check credentials and try again.")
        cache_path = f"data/{symbol}_{exchange}_{interval}.csv"  # Include exchange
        if os.path.exists(cache_path):
            df = pd.read_csv(cache_path, index_col='datetime', parse_dates=True)
            if len(df) >= n_bars:
                return df.iloc[-n_bars:]  # Return last n_bars
        try:
            intv = self.map_interval(interval)
            df = self.tv.get_hist(symbol=symbol, exchange=exchange, interval=intv, n_bars=n_bars)
            if df is not None:
                df.to_csv(cache_path)  # Overwrite cache with new data
                return df
            else:
                raise ValueError("No data fetched from TradingView.")
        except Exception as e:
            raise e

    def get_live_data(self, symbol, exchange, interval):
        if self.tv is None:
            return None
        try:
            intv = self.map_interval(interval)
            new_df = self.live.get_hist(symbol=symbol, exchange=exchange, interval=intv, n_bars=1)
            return new_df
        except:
            return None

    def map_interval(self, interval):
        mapping = {
            '1m': Interval.in_1_minute,
            '5m': Interval.in_5_minute,
            '15m': Interval.in_15_minute,
            '1h': Interval.in_1_hour,
            '4h': Interval.in_4_hour,
            '1D': Interval.in_daily,
            '1W': Interval.in_weekly,
            '1M': Interval.in_monthly
        }
        return mapping.get(interval, Interval.in_daily)