import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses info/warning messages (set to '2' for warnings only, '1' for info only)

from sklearn.ensemble import RandomForestClassifier
from joblib import load, dump
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

class MLModel:
    def __init__(self):
        self.rf_model = self.load_rf_model()
        self.lstm_model = self.load_lstm_model()

    def load_rf_model(self):
        try:
            return load('data/models/rf_model.joblib')
        except:
            # Train simple
            # Assume data
            X = np.random.rand(100,10)
            y = np.random.randint(0,2,100)
            model = RandomForestClassifier()
            model.fit(X, y)
            dump(model, 'data/models/rf_model.joblib')
            return model

    def load_lstm_model(self):
        try:
            return load_model('data/models/lstm.h5')
        except:
            model = Sequential()
            model.add(LSTM(50, input_shape=(10,1)))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mse')
            # Train on dummy
            X = np.random.rand(100,10,1)
            y = np.random.rand(100)
            model.fit(X, y, epochs=5)
            model.save('data/models/lstm.h5')
            return model

    def get_pattern_probability(self, pattern):
        # Extract features from pattern, predict
        features = np.random.rand(1,10)  # Dummy
        return self.rf_model.predict_proba(features)[0][1]

    def predict_future(self, df):
        # Normalize, reshape for LSTM, predict next n steps
        last = df['close'].values[-10:].reshape(1,10,1)
        pred = self.lstm_model.predict(last)[0]
        future_dates = pd.date_range(df.index[-1], periods=10)
        return {'date': future_dates, 'close': np.cumsum(pred) + df['close'][-1]}