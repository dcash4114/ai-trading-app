from pyharmonics.technicals import Technicals
from pyharmonics.search import HarmonicSearch

def detect_harmonic(df, symbol, interval):
    t = Technicals(df, symbol, interval)
    detector = HarmonicSearch(t)
    detector.search()
    patterns = detector.get_patterns()
    # Format to dict list (adjust attributes if needed based on actual pattern object structure)
    return [{'type': p.pattern, 'point': p.points, 'lines': p.lines} for p in patterns]  # Assume structure