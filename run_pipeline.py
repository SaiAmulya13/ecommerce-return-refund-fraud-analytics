"""
Master pipeline runner for E-commerce Fraud Analytics
Runs preprocessing, feature engineering, training & evaluation
"""

import pandas as pd
import subprocess
import sys

print("\n==============================")
print("🚀 STARTING FRAUD PIPELINE")
print("==============================\n")

# -----------------------------
# 1. DATA PREPROCESSING
# -----------------------------
print("📦 Step 1: Data Preprocessing")
subprocess.run([sys.executable, "src/data_preprocessing.py"])

# -----------------------------
# 2. FEATURE ENGINEERING
# -----------------------------
print("\n🛠 Step 2: Feature Engineering")
subprocess.run([sys.executable, "src/feature_engineering.py"])

# -----------------------------
# 3. TRAIN RANDOM FOREST
# -----------------------------
print("\n🌲 Step 3: Train Random Forest")
subprocess.run([sys.executable, "src/train_random_forest.py"])

# -----------------------------
# 4. TRAIN XGBOOST
# -----------------------------
print("\n⚡ Step 4: Train XGBoost")
subprocess.run([sys.executable, "src/train_xgboost.py"])

# -----------------------------
# 5. MODEL EVALUATION
# -----------------------------
print("\n📊 Step 5: Model Evaluation")
subprocess.run([sys.executable, "src/model_evaluation.py"])

print("\n==============================")
print("✅ PIPELINE FINISHED SUCCESSFULLY")
print("==============================")
