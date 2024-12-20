# -*- coding: utf-8 -*-
"""NWH566.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gQJNOD5QeC0p5GAxH4PYFehv1FR5z22k

1. Loading and Understanding the Dataset

Importing the necessary python libararies
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

"""Reading the dataset"""

data = pd.read_csv('/content/GOLD_2022_normalised_NEW-1000.csv')

"""Displaying the first few rows of the dataset"""

data.head()

"""Checking for basic info like column names, data types, and missing values"""

data.info()

"""Descriptive statistics"""

data.describe()

"""2. Exploratory Data Analysis

Checking for Missing Data
"""

missing_values = data.isnull().sum()

"""Feature Distribution: Visualize the distribution of important features like Open_Bid, Close_Bid, Volume_Bid, etc."""

data[['Open_Bid', 'Close_Bid', 'Volume_Bid', 'Volume_Ask', 'Volume_Delta']].hist(figsize=(12, 8))
plt.show()

"""Correlation Analysis"""

corr = data.corr()
plt.figure(figsize=(14, 10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

"""Feature Engineering

Creating additional features that may help improve model performance: 5-day moving average
"""

data['SMA_5'] = data['Close_Bid'].rolling(window=5).mean()

"""Adding percentage change in price"""

data['Price_Change'] = data['Close_Bid'].pct_change()

"""Data Preprocessing for Machine Learning

Feature Selection: Selecting relevant features for training
"""

features = ['Open_Bid', 'High_Bid', 'Low_Bid', 'Close_Bid', 'Volume_Bid', 'SMA_5', 'Price_Change']
target = 'Close_Bid'
X = data[features]
y = data[target]

"""Spliting the data into training and test sets"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

"""Scaling Features"""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""Machine Learning Models: Random Forest Regressor"""

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
y_pred_rf = rf_model.predict(X_test_scaled)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
print(f"Random Forest MAE: {mae_rf}")
print(f"Random Forest MSE: {mse_rf}")

"""Model Evaluation"""

r2_rf = r2_score(y_test, y_pred_rf)
print(f"Random Forest R²: {r2_rf}")

bins = np.linspace(min(y_test), max(y_test), 10)  # 10 bins
y_test_binned = np.digitize(y_test, bins)
y_pred_binned = np.digitize(y_pred_rf, bins)
cm = confusion_matrix(y_test_binned, y_pred_binned)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=bins[:-1], yticklabels=bins[:-1])
plt.title('Confusion Matrix for Binned Regression Predictions')
plt.xlabel('Predicted Binned Values')
plt.ylabel('True Binned Values')
plt.show()

"""Deep Learning Model: ANN"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

file_path = '/content/GOLD_2022_normalised_NEW-1000.csv'
data = pd.read_csv(file_path)

X = data.drop(columns=['Y_High_Bid', 'Y_Low_Ask'])
y = data[['Y_High_Bid', 'Y_Low_Ask']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = Sequential([
    Dense(128, activation='relu', input_dim=X_train_scaled.shape[1]),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(2, activation='linear')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

history = model.fit(
    X_train_scaled, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

evaluation = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Test Loss: {evaluation[0]}")
print(f"Test Mean Absolute Error: {evaluation[1]}")

model.save('ANN_GOLD_model.h5')
print("Model saved as 'ANN_GOLD_model.h5'.")

import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.plot(history.history['mae'], label='Train MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('Model Mean Absolute Error')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()
plt.show()

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np


y_pred = model.predict(X_test_scaled)

threshold_high_bid = y['Y_High_Bid'].median()
threshold_low_ask = y['Y_Low_Ask'].median()
y_pred_classes = np.array([
    [1 if pred[0] >= threshold_high_bid else 0,
     1 if pred[1] >= threshold_low_ask else 0]
    for pred in y_pred
])

y_test_classes = np.array([
    [1 if actual[0] >= threshold_high_bid else 0,
     1 if actual[1] >= threshold_low_ask else 0]
    for actual in y_test.to_numpy()
])
for i, label in enumerate(['Y_High_Bid', 'Y_Low_Ask']):
    cm = confusion_matrix(y_test_classes[:, i], y_pred_classes[:, i])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
    print(f"Confusion Matrix for {label}:")
    disp.plot(cmap='Blues')
    plt.title(f"Confusion Matrix for {label}")
    plt.show()