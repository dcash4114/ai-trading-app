# AI-Powered Trading App



This is a standalone, local desktop application for AI-powered trading analysis, built in Python. 

It integrates with TradingView for data, detects trading patterns and indicators, performs backtesting, 

and provides real-time updates. The app is cross-platform (Windows, macOS, Linux) and uses PyQt6 for the GUI.



### Features

##### &nbsp;	Data Integration: 

&nbsp;		Fetch live and historical OHLCV data from TradingView using user credentials. Supports stocks, 

&nbsp;		forex, commodities, indices, and cryptocurrencies.

##### &nbsp;	Charting: 

&nbsp;		Interactive candlestick charts with zoom, pan, and tooltips, mimicking TradingView's layout.

##### &nbsp;	Indicators and Patterns:

###### &nbsp;		Technical indicators: 

&nbsp;			SMA, EMA, RSI, MACD, Bollinger Bands, etc. (via pandas-ta and TA-Lib equivalents).

###### &nbsp;		Traditional patterns: 

&nbsp;			Head and Shoulders, Double Top/Bottom, Flags, Pennants, etc.

###### &nbsp;		Harmonic patterns: 

&nbsp;			Gartley, Bat, Butterfly, etc. (via pyharmonics).

###### &nbsp;		Fibonacci tools: 

&nbsp;			Retracements, Extensions.

###### &nbsp;		AI enhancements: 

&nbsp;			Pattern probability estimation and short-term price forecasts using ML models 

&nbsp;			(scikit-learn and TensorFlow).

##### &nbsp;	Backtesting: 

&nbsp;		Simulate strategies on historical data, displaying metrics like win rate, profit factor, 

&nbsp;		and max drawdown.

##### &nbsp;	Real-Time Updates: 

&nbsp;		Live data streaming via WebSocket, with automatic chart and indicator refreshes.

##### &nbsp;	Alerts: 

&nbsp;		System tray notifications for high-probability signals.

##### &nbsp;	UI Customization: 

&nbsp;		Dark/light themes, responsive layout, keyboard shortcuts.

##### &nbsp;	Security: 

&nbsp;		Credentials stored encrypted locally using keyring.

##### &nbsp;	Extensibility: 

&nbsp;		Modular design for adding custom indicators.



### Requirements

##### &nbsp;	Python 3.12+

##### &nbsp;	TradingView account (free or paid) for data access.

##### &nbsp;	Dependencies (listed in requirements.txt):

&nbsp;		pandas

&nbsp;		numpy

&nbsp;		pandas-ta

&nbsp;		scipy

&nbsp;		scikit-learn

&nbsp;		tensorflow

&nbsp;		pyqt6

&nbsp;		matplotlib

&nbsp;		tvdatafeed

&nbsp;		keyring

&nbsp;		pyharmonics

&nbsp;		joblib



## Installation

##### &nbsp;	Clone or Download the Project:

&nbsp;		Download the project files or clone the repository if available.

##### &nbsp;	Set Up Virtual Environment (Recommended):

&nbsp;		python -m venv venv

&nbsp;		source venv/bin/activate  # On Linux/macOS

&nbsp;		venv\\Scripts\\activate     # On Windows

##### &nbsp;	Install Dependencies:

&nbsp;		pip install -r requirements.txt

##### &nbsp;	Prepare Data and Models Directory:

&nbsp;		Create data/ folder if not present (for caching historical data and models).

&nbsp;		Create data/models/ for ML model files (app will generate them if missing).

##### &nbsp;	Run Tests (Optional):

&nbsp;		python -m unittest discover tests



### Usage

##### &nbsp;	Launch the App:

&nbsp;		python main.py

##### &nbsp;	Initial Setup:

&nbsp;		On first launch, a dialog will prompt for TradingView username and password. 

&nbsp;		These are stored securely locally. If credentials change, delete them via 

&nbsp;		keyring (e.g., using keyring CLI) and relaunch.

##### &nbsp;	Main Interface:

###### &nbsp;		Central Chart: 

&nbsp;			Displays candlestick chart for the selected symbol and timeframe. 

&nbsp;			Use toolbar for zoom/pan.

###### &nbsp;		Left Sidebar:

&nbsp;			Symbol: Enter ticker (e.g., AAPL, BTCUSD:BINANCE).

&nbsp;			Interval: Select timeframe (1m, 5m, etc.).

&nbsp;			Load Data: Fetch and display data.

&nbsp;			Indicators/Patterns: Checkboxes to toggle (e.g., SMA, Head and Shoulders, 

&nbsp;			Harmonic Patterns).

&nbsp;			Run Backtest: Simulate on historical data using selected indicators/patterns.

&nbsp;			Switch Theme: Toggle dark/light mode.

###### &nbsp;		Real-Time Updates: 

&nbsp;			Chart updates every 5 seconds with new data.

###### &nbsp;		Alerts: 

&nbsp;			Pop-ups for patterns with >80% probability.

###### &nbsp;		Keyboard Shortcuts: 

&nbsp;			Ctrl+Z for zoom out (extendable).

##### &nbsp;	Viewing Patterns and Signals:

&nbsp;		Detected patterns appear on the chart with lines, labels, and probability tooltips.

&nbsp;		Buy/sell points: Annotated with arrows; targets based on pattern rules.

&nbsp;		Predictions: Shaded forecast areas for future prices.

##### &nbsp;	Backtesting:

&nbsp;		Select period via data load (historical data cached).

&nbsp;		Results shown in a dialog: Win rate, etc.

&nbsp;		Historical signals overlaid on chart.

##### &nbsp;	Customizations:

###### &nbsp;		Add custom indicators: 

&nbsp;			Create scripts in indicators/ and import in pattern\_detector.py or 

&nbsp;			indicator\_calculator.py.

###### &nbsp;		Themes: 

&nbsp;			Edit utils/helpers.py for styles.

###### &nbsp;		Logging: 

&nbsp;			Check log.txt for debug info.

##### &nbsp;	Troubleshooting:

###### &nbsp;		API Errors: 

&nbsp;			Check credentials; handle rate limits (app reconnects automatically).

###### &nbsp;		Data Issues: 

&nbsp;			Ensure symbol/exchange format (e.g., AAPL:NASDAQ).

###### &nbsp;		Performance: 

&nbsp;			Limit historical bars if slow; app optimizes with caching.

###### &nbsp;		ML Models: 

&nbsp;			App trains simple models on dummy data initially; for better accuracy, 

&nbsp;			provide real datasets in ml\_model.py.

### Limitations

&nbsp;	Relies on TradingView API; subject to their limits and availability.

&nbsp;	ML models are basic; enhance with custom training data.

&nbsp;	No real trading execution; analysis only.

&nbsp;	Video/image handling not integrated; focus on charts.

### Contributing

&nbsp;	Fork and PR for improvements (e.g., more patterns, better ML).

&nbsp;	Report issues via logs.

### License

&nbsp;	MIT License (or specify as needed).

