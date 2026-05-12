import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("final dataset.csv")

# Fix column names
df.columns = df.columns.str.strip()

# Remove unnecessary column
df = df.drop(['user'], axis=1)

# -------------------------------
# ✅ DATASET CHECKING (ADD HERE)
# -------------------------------

print("----- DATASET INFO -----")
print(df.info())

print("\n----- MISSING VALUES -----")
print(df.isnull().sum())

print("\n----- DATA TYPES -----")
print(df.dtypes)

print("\n----- FIRST 5 ROWS -----")
print(df.head())

# -------------------------------
# ML PART STARTS HERE
# -------------------------------

# Features
X = df[['cpm','dwell_avg','flight_avg','pressure_touch',
        'scroll_x','scroll_y','tilt_angle']]

# Label
y = df['label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
print("\nAccuracy:", model.score(X_test, y_test))
# Accuracy
print("\nAccuracy:", model.score(X_test, y_test))

# -------------------------------
# SAVE MODEL (IMPORTANT)
# -------------------------------
import pickle

with open("behavior_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully ")