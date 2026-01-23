import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import joblib
import os

# Load data
df = pd.read_csv("data/ecommerce_data.csv")

# Encode categorical column
le = LabelEncoder()
df["payment_method"] = le.fit_transform(df["payment_method"])

# Features and target
X = df.drop("fraud_label", axis=1)
y = df["fraud_label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train XGBoost model
model = XGBClassifier(
    n_estimators=150,
    learning_rate=0.1,
    max_depth=6,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# Ensure models folder exists
os.makedirs("models", exist_ok=True)

# Save model
joblib.dump(model, "models/xgboost.pkl")

print("✅ XGBoost model trained and saved successfully")
