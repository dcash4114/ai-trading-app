import pandas_ta as ta
import mplfinance as mpf
import logging

class IndicatorCalculator:
    def __init__(self):
        pass

    def get_addplots(self, df, indicators):
        addplots = []
        if 'close' not in df.columns:
            logging.warning("Missing 'close' column; cannot calculate indicators.")
            return addplots
        try:
            # Trend indicators on panel 0 (price overlay)
            if "SMA" in indicators:
                sma = ta.sma(df['close'], length=20)
                if sma is not None and not sma.dropna().empty:
                    addplots.append(mpf.make_addplot(sma, panel=0, color='blue', label='SMA'))
            if "EMA" in indicators:
                ema = ta.ema(df['close'], length=20)
                if ema is not None and not ema.dropna().empty:
                    addplots.append(mpf.make_addplot(ema, panel=0, color='red', label='EMA'))
            if "Bollinger Bands" in indicators:
                bb = ta.bbands(df['close'])
                if bb is not None and not bb.dropna().empty:
                    addplots.append(mpf.make_addplot(bb['BBU_5_2.0'], panel=0, color='gray', linestyle='--', label='BB Upper'))
                    addplots.append(mpf.make_addplot(bb['BBM_5_2.0'], panel=0, color='gray', label='BB Middle'))
                    addplots.append(mpf.make_addplot(bb['BBL_5_2.0'], panel=0, color='gray', linestyle='--', label='BB Lower'))

            # Oscillators on separate panels
            panel = 1
            if "RSI" in indicators:
                rsi = ta.rsi(df['close'])
                if rsi is not None and not rsi.dropna().empty:
                    addplots.append(mpf.make_addplot(rsi, panel=panel, color='orange', ylabel='RSI'))
                panel += 1
            if "MACD" in indicators:
                macd = ta.macd(df['close'])
                if macd is not None and not macd.dropna().empty:
                    addplots.append(mpf.make_addplot(macd['MACD_12_26_9'], panel=panel, color='blue', label='MACD'))
                    addplots.append(mpf.make_addplot(macd['MACDs_12_26_9'], panel=panel, color='orange', label='Signal'))
                    addplots.append(mpf.make_addplot(macd['MACDh_12_26_9'], type='bar', panel=panel, color='dimgray', alpha=0.5, ylabel='MACD Hist'))
                panel += 1
            # Add more indicators similarly
        except Exception as e:
            logging.error(f"Error creating addplots: {e}")
        return addplots