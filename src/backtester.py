class Backtester:
    def __init__(self):
        pass

    def run(self, df, strategies):
        # Generate signals based on strategies
        signals = [None] * len(df)  # Initialize with None to match df length
        if 'SMA' in strategies:
            df['SMA_20'] = df['close'].rolling(20).mean()
            df['SMA_50'] = df['close'].rolling(50).mean()
            for i in range(1, len(df)):
                if df['SMA_20'].iloc[i-1] < df['SMA_50'].iloc[i-1] and df['SMA_20'].iloc[i] > df['SMA_50'].iloc[i]:
                    signals[i] = 'buy'
                elif df['SMA_20'].iloc[i-1] > df['SMA_50'].iloc[i-1] and df['SMA_20'].iloc[i] < df['SMA_50'].iloc[i]:
                    signals[i] = 'sell'
        # Add logic for other strategies, e.g., RSI < 30 buy, >70 sell
        if 'RSI' in strategies:
            rsi = ta.rsi(df['close'])
            for i in range(1, len(df)):
                if rsi.iloc[i] < 30:
                    signals[i] = 'buy' if signals[i] is None else signals[i]
                elif rsi.iloc[i] > 70:
                    signals[i] = 'sell' if signals[i] is None else signals[i]
        # For patterns, assume patterns have 'signal' key like 'buy' or 'sell' at certain indices
        # But since patterns are detected separately, perhaps integrate from pattern_detector
        # For now, dummy if no strategies
        if not strategies:
            return {'win_rate': 0, 'profit_factor': 0, 'max_drawdown': 0}

        # Backtest loop
        equity = 10000
        position = 0
        trades = []
        for i in range(len(df)):
            if signals[i] == 'buy' and position == 0:
                position = equity / df['close'].iloc[i]
                entry = df['close'].iloc[i]
            elif signals[i] == 'sell' and position > 0:
                exit_price = df['close'].iloc[i]
                equity = position * exit_price
                profit = (exit_price - entry) / entry
                trades.append(profit)
                position = 0
        # Calculate metrics
        if not trades:
            return {'win_rate': 0, 'profit_factor': 0, 'max_drawdown': 0}
        win_rate = len([t for t in trades if t > 0]) / len(trades)
        profit_factor = sum([t for t in trades if t > 0]) / abs(sum([t for t in trades if t < 0])) if any(t < 0 for t in trades) else float('inf')
        cum_returns = pd.Series(trades).cumsum()
        max_dd = (cum_returns - cum_returns.cummax()).min()
        metrics = {'win_rate': win_rate, 'profit_factor': profit_factor, 'max_drawdown': max_dd}
        return metrics