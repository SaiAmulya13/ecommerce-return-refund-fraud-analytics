import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("data/ecommerce_data.csv")

# Encode categorical column (same as training)
le = LabelEncoder()
df["payment_method"] = le.fit_transform(df["payment_method"])

# Split features and target
X = df.drop("fraud_label", axis=1)
y = df["fraud_label"]

# Load trained model
model = joblib.load("models/random_forest.pkl")

# Predictions
y_pred = model.predict(X)

# Evaluation
print("Confusion Matrix:")
print(confusion_matrix(y, y_pred))

print("\nClassification Report:")
print(classification_report(y, y_pred))
