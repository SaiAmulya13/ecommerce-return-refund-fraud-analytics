import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
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

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# Ensure models folder exists
os.makedirs("models", exist_ok=True)

# Save model
joblib.dump(model, "models/random_forest.pkl")

print("✅ Random Forest model trained and saved successfully")
