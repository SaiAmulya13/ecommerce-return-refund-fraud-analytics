# import streamlit as st
# import pandas as pd
# import joblib

# # -------------------------------
# # Page Config
# # -------------------------------
# st.set_page_config(page_title="Fraud Analytics Dashboard", layout="wide")

# st.title("🛍️ E-commerce Return & Refund Fraud Dashboard")

# # -------------------------------
# # Session State for User Tracking
# # -------------------------------
# if "fraud_tracker" not in st.session_state:
#     st.session_state.fraud_tracker = {}

# # -------------------------------
# # Load Model & Data
# # -------------------------------
# model = joblib.load("models/random_forest.pkl")
# df = pd.read_csv("data/ecommerce_data.csv")

# payment_map = {
#     "Credit Card": 0,
#     "Debit Card": 1,
#     "UPI": 2,
#     "Net Banking": 3,
#     "Cash on Delivery": 4
# }

# # -------------------------------
# # SIDEBAR INPUTS
# # -------------------------------
# st.sidebar.header("🔍 Transaction Details")

# user_id = st.sidebar.number_input("User ID", min_value=1, step=1)
# order_id = st.sidebar.text_input("Order ID")

# order_value = st.sidebar.number_input("Order Value (₹)", 100, 20000, 2000)
# return_count = st.sidebar.slider("Previous Return Count", 0, 20, 1)
# refund_amount = st.sidebar.number_input("Refund Amount (₹)", 0, 20000, 500)
# days_since_order = st.sidebar.slider("Days Since Order", 1, 60, 5)

# payment_method = st.sidebar.selectbox(
#     "Payment Method",
#     list(payment_map.keys())
# )

# is_repeat_customer = st.sidebar.selectbox(
#     "Repeat Customer?",
#     ["Yes", "No"]
# )

# repeat_val = 1 if is_repeat_customer == "Yes" else 0
# refund_ratio = round(refund_amount / order_value, 2)

# # -------------------------------
# # PREDICTION
# # -------------------------------
# if st.sidebar.button("🚨 Analyze Refund Request"):

#     input_df = pd.DataFrame([{
#         "user_id": user_id,
#         "order_value": order_value,
#         "return_count": return_count,
#         "refund_amount": refund_amount,
#         "days_since_order": days_since_order,
#         "payment_method": payment_map[payment_method],
#         "is_repeat_customer": repeat_val,
#         "refund_ratio": refund_ratio
#     }])

#     prediction = model.predict(input_df)[0]
#     prob = model.predict_proba(input_df)[0][1]

#     st.subheader("📊 Decision Result")

#     # Initialize fraud count
#     if user_id not in st.session_state.fraud_tracker:
#         st.session_state.fraud_tracker[user_id] = 0

#     # -------------------------------
#     # FRAUD CASE
#     # -------------------------------
#     if prediction == 1:

#         # LOW RETURN COUNT → Soft review only
#         if return_count <= 1:
#             st.info(
#                 f"🔍 Manual Review Needed for Order {order_id}\n\n"
#                 f"Unusual pattern detected, but not enough history for warning.\n"
#                 f"Risk Score: {prob:.2f}"
#             )

#         else:
#             # Increase fraud count
#             st.session_state.fraud_tracker[user_id] += 1
#             count = st.session_state.fraud_tracker[user_id]

#             if count == 1:
#                 st.warning(
#                     f"⚠️ WARNING to User {user_id} (Order {order_id})\n\n"
#                     f"Suspicious refund behavior detected.\n"
#                     f"Risk Score: {prob:.2f}"
#                 )
#             else:
#                 st.error(
#                     f"🚫 USER {user_id} BLOCKED\n\n"
#                     f"Multiple fraudulent refund attempts detected.\n"
#                     f"Risk Score: {prob:.2f}"
#                 )

#     # -------------------------------
#     # LEGIT CASE
#     # -------------------------------
#     else:
#         st.success(
#             f"✅ Refund Approved for Order {order_id}\n\n"
#             "You will receive your refund shortly."
#         )

# # -------------------------------
# # DATASET OVERVIEW
# # -------------------------------
# st.divider()

# st.subheader("📈 Historical Fraud Summary")

# col1, col2 = st.columns(2)
# col1.metric("Total Transactions", len(df))
# col2.metric("Fraud Cases", int(df["fraud_label"].sum()))

# st.bar_chart(df["fraud_label"].value_counts())

# # -------------------------------
# # ADMIN VIEW
# # -------------------------------
# st.divider()
# st.subheader("🛑 Flagged Users (Session)")

# if st.session_state.fraud_tracker:
#     fraud_df = pd.DataFrame(
#         st.session_state.fraud_tracker.items(),
#         columns=["User ID", "Fraud Attempts"]
#     )
#     st.dataframe(fraud_df)
# else:
#     st.info("No users flagged yet.")
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -------------------------------
# BASE DIRECTORY (Cloud Safe)
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "random_forest.pkl"
DATA_PATH = BASE_DIR / "data" / "ecommerce_data.csv"

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Fraud Analytics Dashboard", layout="wide")

st.title("🛍️ E-commerce Return & Refund Fraud Dashboard")

# -------------------------------
# Session State for User Tracking
# -------------------------------
if "fraud_tracker" not in st.session_state:
    st.session_state.fraud_tracker = {}

# -------------------------------
# Load Model & Data
# -------------------------------
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

payment_map = {
    "Credit Card": 0,
    "Debit Card": 1,
    "UPI": 2,
    "Net Banking": 3,
    "Cash on Delivery": 4
}

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🔍 Transaction Details")

user_id = st.sidebar.number_input("User ID", min_value=1, step=1)
order_id = st.sidebar.text_input("Order ID")

order_value = st.sidebar.number_input("Order Value (₹)", 100, 20000, 2000)
return_count = st.sidebar.slider("Previous Return Count", 0, 20, 1)
refund_amount = st.sidebar.number_input("Refund Amount (₹)", 0, 20000, 500)
days_since_order = st.sidebar.slider("Days Since Order", 1, 60, 5)

payment_method = st.sidebar.selectbox(
    "Payment Method",
    list(payment_map.keys())
)

is_repeat_customer = st.sidebar.selectbox(
    "Repeat Customer?",
    ["Yes", "No"]
)

repeat_val = 1 if is_repeat_customer == "Yes" else 0
refund_ratio = round(refund_amount / order_value, 2)

# -------------------------------
# PREDICTION
# -------------------------------
if st.sidebar.button("🚨 Analyze Refund Request"):

    input_df = pd.DataFrame([{
        "user_id": user_id,
        "order_value": order_value,
        "return_count": return_count,
        "refund_amount": refund_amount,
        "days_since_order": days_since_order,
        "payment_method": payment_map[payment_method],
        "is_repeat_customer": repeat_val,
        "refund_ratio": refund_ratio
    }])

    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    st.subheader("📊 Decision Result")

    # Initialize fraud count
    if user_id not in st.session_state.fraud_tracker:
        st.session_state.fraud_tracker[user_id] = 0

    # -------------------------------
    # FRAUD CASE
    # -------------------------------
    if prediction == 1:

        # LOW RETURN COUNT → Soft review only
        if return_count <= 1:
            st.info(
                f"🔍 Manual Review Needed for Order {order_id}\n\n"
                f"Unusual pattern detected, but not enough history for warning.\n"
                f"Risk Score: {prob:.2f}"
            )

        else:
            # Increase fraud count
            st.session_state.fraud_tracker[user_id] += 1
            count = st.session_state.fraud_tracker[user_id]

            if count == 1:
                st.warning(
                    f"⚠️ WARNING to User {user_id} (Order {order_id})\n\n"
                    f"Suspicious refund behavior detected.\n"
                    f"Risk Score: {prob:.2f}"
                )
            else:
                st.error(
                    f"🚫 USER {user_id} BLOCKED\n\n"
                    f"Multiple fraudulent refund attempts detected.\n"
                    f"Risk Score: {prob:.2f}"
                )

    # -------------------------------
    # LEGIT CASE
    # -------------------------------
    else:
        st.success(
            f"✅ Refund Approved for Order {order_id}\n\n"
            "You will receive your refund shortly."
        )

# -------------------------------
# DATASET OVERVIEW
# -------------------------------
st.divider()

st.subheader("📈 Historical Fraud Summary")

col1, col2 = st.columns(2)
col1.metric("Total Transactions", len(df))
col2.metric("Fraud Cases", int(df["fraud_label"].sum()))

st.bar_chart(df["fraud_label"].value_counts())

# -------------------------------
# ADMIN VIEW
# -------------------------------
st.divider()
st.subheader("🛑 Flagged Users (Session)")

if st.session_state.fraud_tracker:
    fraud_df = pd.DataFrame(
        st.session_state.fraud_tracker.items(),
        columns=["User ID", "Fraud Attempts"]
    )
    st.dataframe(fraud_df)
else:
    st.info("No users flagged yet.")
