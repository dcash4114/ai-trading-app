from scipy.signal import find_peaks

def detect_traditional(df):
    patterns = []
    
    # Detect Head and Shoulders (example implementation; expand for other patterns)
    close = df['close'].values
    peaks, props = find_peaks(close, prominence=0.05 * close.mean(), distance=10)
    if len(peaks) >= 3:
        # Check if peaks[1] > peaks[0] and peaks[2], for H&S
        if close[peaks[1]] > close[peaks[0]] and close[peaks[1]] > close[peaks[2]] and abs(close[peaks[0]] - close[peaks[2]]) < 0.02 * close[peaks[1]]:
            # Define lines as pairs of (x, y) for plotting (e.g., neckline, shoulders)
            # Example: Connect left shoulder to right shoulder
            neckline_x = [df.index[peaks[0]], df.index[peaks[2]]]
            neckline_y = [close[peaks[0]], close[peaks[2]]]
            patterns.append({
                'type': 'Head and Shoulders', 
                'point': (df.index[peaks[1]], close[peaks[1]]),  # Head point for annotation
                'lines': [(neckline_x, neckline_y)],  # List of line segments
                'text': 'H&S'
            })
    
    # Add detection for other traditional patterns here (e.g., Double Top, Flags)
    # Example placeholder for Double Top:
    # troughs = find_peaks(-close, prominence=0.05 * close.mean(), distance=10)[0]
    # if len(peaks) >= 2 and similar heights:
    #     patterns.append({...})
    
    return patterns