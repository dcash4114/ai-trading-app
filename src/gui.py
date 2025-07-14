from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QDockWidget, QComboBox, QCheckBox, QPushButton, QLabel, 
    QLineEdit, QDialog, QFormLayout, QSystemTrayIcon, QMenu, QMessageBox, QSplitter
)
from PyQt6.QtGui import QIcon, QPalette, QColor, QAction
from PyQt6.QtCore import QTimer, Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import mplfinance as mpf
from src.data_manager import DataManager
from src.pattern_detector import PatternDetector
from src.indicator_calculator import IndicatorCalculator
from src.backtester import Backtester
from src.ml_model import MLModel
from utils.helpers import setup_logging, get_theme_stylesheet
import logging
import keyring
import pandas as pd

class CredentialsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TradingView Credentials")
        layout = QFormLayout()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Username:", self.username_edit)
        layout.addRow("Password:", self.password_edit)
        buttons = QWidget()
        btn_layout = QVBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        buttons.setLayout(btn_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Powered Trading App")
        self.setGeometry(100, 100, 1200, 800)
        self.data_manager = DataManager()
        self.pattern_detector = PatternDetector()
        self.indicator_calculator = IndicatorCalculator()
        self.backtester = Backtester()
        self.ml_model = MLModel()
        self.current_symbol = "AAPL"
        self.current_exchange = "NASDAQ"
        self.current_interval = "1D"
        self.current_time_frame = "1Y"
        self.df = None
        self.live_timer = QTimer(self)
        self.live_timer.timeout.connect(self.update_data)
        self.live_timer.start(5000)  # Update every 5 seconds
        self.setup_ui()
        self.setup_theme("dark")
        self.check_credentials()
        self.load_data()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QSplitter(Qt.Orientation.Horizontal)
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().addWidget(main_layout)

        # Chart area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        chart_widget = QWidget()
        chart_layout = QVBoxLayout()
        chart_layout.addWidget(self.toolbar)
        chart_layout.addWidget(self.canvas)
        chart_widget.setLayout(chart_layout)
        main_layout.addWidget(chart_widget)

        # Sidebar
        sidebar = QDockWidget("Controls", self)
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        self.symbol_edit = QLineEdit(self.current_symbol)
        self.exchange_edit = QLineEdit(self.current_exchange)
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"])
        self.interval_combo.setCurrentText(self.current_interval)
        self.time_frame_combo = QComboBox()
        self.time_frame_combo.addItems(["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"])
        self.time_frame_combo.setCurrentText(self.current_time_frame)
        load_btn = QPushButton("Load Data")
        load_btn.clicked.connect(self.load_data)
        self.interval_combo.currentIndexChanged.connect(self.load_data)
        self.time_frame_combo.currentIndexChanged.connect(self.load_data)
        sidebar_layout.addWidget(QLabel("Symbol:"))
        sidebar_layout.addWidget(self.symbol_edit)
        sidebar_layout.addWidget(QLabel("Exchange:"))
        sidebar_layout.addWidget(self.exchange_edit)
        sidebar_layout.addWidget(QLabel("Interval:"))
        sidebar_layout.addWidget(self.interval_combo)
        sidebar_layout.addWidget(QLabel("Time Frame:"))
        sidebar_layout.addWidget(self.time_frame_combo)
        sidebar_layout.addWidget(load_btn)

        # Indicator toggles
        self.indicator_checkboxes = {}
        indicators = ["SMA", "EMA", "RSI", "MACD", "Bollinger Bands", "Head and Shoulders", "Harmonic Patterns", "Fibonacci Retracements"]
        for ind in indicators:
            cb = QCheckBox(ind)
            cb.toggled.connect(self.update_chart)
            self.indicator_checkboxes[ind] = cb
            sidebar_layout.addWidget(cb)

        # Backtest button
        backtest_btn = QPushButton("Run Backtest")
        backtest_btn.clicked.connect(self.run_backtest)
        sidebar_layout.addWidget(backtest_btn)

        # Theme switch
        theme_btn = QPushButton("Switch Theme")
        theme_btn.clicked.connect(self.switch_theme)
        sidebar_layout.addWidget(theme_btn)

        sidebar_widget.setLayout(sidebar_layout)
        sidebar.setWidget(sidebar_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sidebar)

        # Tray for alerts
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon.fromTheme("dialog-information"))
        menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        menu.addAction(show_action)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def setup_theme(self, theme):
        if theme == "dark":
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            self.setPalette(palette)
            self.setStyleSheet(get_theme_stylesheet("dark"))
        else:
            self.setPalette(QPalette())  # Default light
            self.setStyleSheet(get_theme_stylesheet("light"))

    def switch_theme(self):
        current = self.styleSheet()
        if "dark" in current:
            self.setup_theme("light")
        else:
            self.setup_theme("dark")

    def check_credentials(self):
        username = keyring.get_password("tradingapp", "tv_username")
        password = keyring.get_password("tradingapp", "tv_password")
        if not username or not password:
            dialog = CredentialsDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                username = dialog.username_edit.text()
                password = dialog.password_edit.text()
                keyring.set_password("tradingapp", "tv_username", username)
                keyring.set_password("tradingapp", "tv_password", password)
                if not self.data_manager.login(username, password):
                    QMessageBox.warning(self, "Login Failed", "Invalid TradingView credentials. Please try again.")
                    return
        else:
            if not self.data_manager.login(username, password):
                QMessageBox.warning(self, "Login Failed", "Invalid TradingView credentials. Please update them.")
                return

    def calculate_n_bars(self, interval, time_frame):
        time_frame_trading_days = {'1D': 1, '1W': 5, '1M': 21, '3M': 63, '6M': 126, '1Y': 252, '5Y': 1260}
        interval_min = {'1m': 1, '5m': 5, '15m': 15, '1h': 60, '4h': 240}
        if interval in interval_min:
            bars_per_day = 390 / interval_min[interval]  # US trading minutes
        elif interval == '1D':
            bars_per_day = 1
        elif interval == '1W':
            bars_per_day = 1 / 5
        elif interval == '1M':
            bars_per_day = 1 / 21
        else:
            bars_per_day = 1
        n_bars = int(time_frame_trading_days[time_frame] * bars_per_day)
        return min(max(n_bars, 100), 5000)

    def load_data(self):
        self.current_symbol = self.symbol_edit.text().upper()
        self.current_exchange = self.exchange_edit.text().upper()
        self.current_interval = self.interval_combo.currentText()
        self.current_time_frame = self.time_frame_combo.currentText()
        self.current_n_bars = self.calculate_n_bars(self.current_interval, self.current_time_frame)
        try:
            self.df = self.data_manager.get_historical_data(self.current_symbol, self.current_exchange, self.current_interval, self.current_n_bars)
            if self.df is None or not isinstance(self.df, pd.DataFrame) or self.df.empty:
                raise ValueError("No data returned. Check symbol, exchange, interval, or TradingView credentials.")
            self.update_chart()
        except Exception as e:
            logging.error(f"Data load error: {e}")
            QMessageBox.warning(self, "Error", str(e))

    def update_data(self):
        if self.df is not None:
            new_data = self.data_manager.get_live_data(self.current_symbol, self.current_exchange, self.current_interval)
            if new_data is not None:
                self.df = pd.concat([self.df, new_data]).drop_duplicates()
                self.update_chart()
                self.check_alerts()

    def update_chart(self):
        if self.df is None or not isinstance(self.df, pd.DataFrame) or self.df.empty:
            return
        self.figure.clear()
        indicators = [k for k, v in self.indicator_checkboxes.items() if v.isChecked()]
        addplots = self.indicator_calculator.get_addplots(self.df, indicators)
        fig, axes = mpf.plot(self.df, type='candle', returnfig=True, addplot=addplots, volume=False, style='yahoo')
        if isinstance(axes, list):
            price_ax = axes[0]
        else:
            price_ax = axes
        # Add patterns
        patterns = self.pattern_detector.detect(self.df, self.current_symbol, self.current_interval, indicators)
        has_legend = False
        for p in patterns:
            if 'lines' in p:
                for line in p['lines']:
                    price_ax.plot(line[0], line[1], linestyle='--', color='yellow')
            if 'text' in p and 'point' in p:
                price_ax.annotate(p['text'], xy=p['point'], color='red')
            prob = self.ml_model.get_pattern_probability(p)
            if 'point' in p:
                price_ax.annotate(f"{p['type']} ({prob:.0%})", xy=p['point'], color='blue')
        # Add predictions
        if 'prediction' in indicators:
            forecast = self.ml_model.predict_future(self.df)
            price_ax.plot(forecast['date'], forecast['close'], linestyle='--', color='green', label='Forecast')
            has_legend = True
        # Only call legend if there are labeled artists
        if has_legend or addplots:  # If predictions or indicators added
            price_ax.legend()

        # Auto date formatter for dynamic scaling
        for a in axes if isinstance(axes, list) else [axes]:
            a.xaxis.set_major_locator(mdates.AutoDateLocator())
            a.xaxis.set_major_formatter(mdates.ConciseDateFormatter(a.xaxis.get_major_locator()))

        self.canvas.draw()

    def on_xlim_changed(self, ax):
        left, right = ax.get_xlim()
        if len(self.df) == 0:
            return
        earliest_num = mdates.date2num(self.df.index[0])
        if left < earliest_num - 1:
            self.current_n_bars += 100
            try:
                new_df = self.data_manager.get_historical_data(self.current_symbol, self.current_exchange, self.current_interval, self.current_n_bars)
                if new_df is not None and len(new_df) > len(self.df):
                    self.df = new_df
                    self.update_chart()
                    ax.set_xlim(left, right)
                    self.canvas.draw()
            except Exception as e:
                logging.error(f"Error loading more data: {e}")

    def run_backtest(self):
        if self.df is None or not isinstance(self.df, pd.DataFrame) or self.df.empty:
            QMessageBox.warning(self, "Error", "No data loaded. Load data first.")
            return
        results = [k for k, v in self.indicator_checkboxes.items() if v.isChecked()]
        metrics = self.backtester.run(self.df, results)
        QMessageBox.information(self, "Backtest Results", str(metrics))

    def check_alerts(self):
        if self.df is None or not isinstance(self.df, pd.DataFrame) or self.df.empty:
            return
        patterns = self.pattern_detector.detect(self.df[-10:], self.current_symbol, self.current_interval, [])
        for p in patterns:
            prob = self.ml_model.get_pattern_probability(p)
            if prob > 0.8:
                self.tray.showMessage("Alert", f"{p['type']} detected with {self.current_symbol} prob {prob:.0%}")

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Z:
            # Zoom out
            pass  # Implement zoom out