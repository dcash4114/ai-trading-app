from scipy.signal import find_peaks
from indicators.harmonic import detect_harmonic
from indicators.traditional import detect_traditional
class PatternDetector:
    def __init__(self):
        pass

    def detect(self, df, symbol, interval, selected):
        patterns = []
        if 'Head and Shoulders' in selected:
            patterns += detect_traditional(df)  # Changed from detect_traditional.head_and_shoulders(df)
        if 'Harmonic Patterns' in selected:
            patterns += detect_harmonic(df, symbol, interval)
        # Add more
        if 'Fibonacci Retracements' in selected:
            patterns += self.detect_fib(df)
        return patterns

    def detect_fib(self, df):
        # Simple fib levels based on recent high/low
        high = max(df['high'].iloc[-50:])
        low = min(df['low'].iloc[-50:])
        levels = [low + (high - low) * level for level in [0, 0.236, 0.382, 0.5, 0.618, 1.0]]
        # Return lines
        return [{'type': 'fib', 'levels': levels}]