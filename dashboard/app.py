import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Fraud Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🛍️ E-Commerce Return & Refund Fraud Dashboard")
st.subheader("Real-Time Fraud Detection & Risk Analysis")

# ============================================================
# FIND DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

possible_files = [
    BASE_DIR / "dataset_with_risk.csv",
    BASE_DIR / "data" / "dataset_with_risk.csv",
    BASE_DIR / "ecommerce_data.csv",
    BASE_DIR / "data" / "ecommerce_data.csv",
]

DATA_PATH = None

for file_path in possible_files:
    if file_path.exists():
        DATA_PATH = file_path
        break

# ============================================================
# LOAD DATASET
# ============================================================

if DATA_PATH is None:

    st.error(
        "❌ Dataset not found.\n\n"
        "Please keep dataset_with_risk.csv in the same folder "
        "as fraud_dashboard.py."
    )

    st.stop()

try:

    df = pd.read_csv(DATA_PATH)

    st.success("✅ Dataset loaded successfully")

except Exception as e:

    st.error(f"❌ Error loading dataset: {e}")
    st.stop()

# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# ============================================================
# CREATE ORDER VALUE IF MISSING
# ============================================================

if "order_value" not in df.columns:

    if "product_price" in df.columns and "order_quantity" in df.columns:

        df["order_value"] = (
            pd.to_numeric(df["product_price"], errors="coerce")
            *
            pd.to_numeric(df["order_quantity"], errors="coerce")
        )

    elif "product_price" in df.columns:

        df["order_value"] = pd.to_numeric(
            df["product_price"],
            errors="coerce"
        )

    else:

        df["order_value"] = 0

# ============================================================
# CREATE REFUND AMOUNT IF MISSING
# ============================================================

if "refund_amount" not in df.columns:

    if "order_value" in df.columns:

        df["refund_amount"] = 0.0

    else:

        df["refund_amount"] = 0.0

# ============================================================
# CREATE DAYS TO RETURN IF MISSING
# ============================================================

if "days_to_return" not in df.columns:

    if "return_date" in df.columns and "order_date" in df.columns:

        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

        df["return_date"] = pd.to_datetime(
            df["return_date"],
            errors="coerce"
        )

        df["days_to_return"] = (
            df["return_date"] - df["order_date"]
        ).dt.days

    else:

        df["days_to_return"] = 0

# ============================================================
# CREATE REFUND RATIO
# ============================================================

if "refund_ratio" not in df.columns:

    df["refund_ratio"] = 0.0

    valid_orders = df["order_value"] > 0

    df.loc[valid_orders, "refund_ratio"] = (
        df.loc[valid_orders, "refund_amount"]
        /
        df.loc[valid_orders, "order_value"]
    )

# ============================================================
# CREATE FRAUD LABEL
# ============================================================

fraud_column = None

possible_fraud_columns = [
    "is_fraud",
    "fraud",
    "fraud_label",
    "risk",
    "risk_label"
]

for col in possible_fraud_columns:

    if col in df.columns:

        fraud_column = col
        break

# ============================================================
# FRAUD SUMMARY
# ============================================================

st.divider()

st.header("📊 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    len(df)
)

if fraud_column is not None:

    try:

        fraud_values = pd.to_numeric(
            df[fraud_column],
            errors="coerce"
        ).fillna(0)

        fraud_count = int(
            (fraud_values == 1).sum()
        )

    except:

        fraud_count = 0

else:

    fraud_count = 0

col2.metric(
    "Fraud Cases",
    fraud_count
)

col3.metric(
    "Average Order Value",
    f"₹{df['order_value'].mean():,.2f}"
)

col4.metric(
    "Average Refund",
    f"₹{df['refund_amount'].mean():,.2f}"
)

# ============================================================
# DATA PREVIEW
# ============================================================

st.divider()

st.header("📋 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

# ============================================================
# FRAUD DISTRIBUTION
# ============================================================

if fraud_column is not None:

    st.divider()

    st.header("🚨 Fraud Distribution")

    fraud_data = pd.to_numeric(
        df[fraud_column],
        errors="coerce"
    ).fillna(0)

    fraud_counts = fraud_data.value_counts()

    chart_df = pd.DataFrame({
        "Transaction Type": [
            "Legitimate" if value == 0 else "Fraud"
            for value in fraud_counts.index
        ],
        "Count": fraud_counts.values
    })

    st.bar_chart(
        chart_df.set_index("Transaction Type")
    )

# ============================================================
# REAL-TIME REFUND ANALYSIS
# ============================================================

st.divider()

st.header("🔍 Real-Time Refund Risk Analysis")

st.write(
    "Enter transaction details below to analyze the refund risk."
)

left, right = st.columns(2)

with left:

    user_id = st.text_input(
        "User ID",
        "USER00000001"
    )

    order_id = st.text_input(
        "Order ID",
        "ORD00000001"
    )

    product_price = st.number_input(
        "Product Price (₹)",
        min_value=0.0,
        value=500.0,
        step=50.0
    )

    order_quantity = st.number_input(
        "Order Quantity",
        min_value=1,
        value=1,
        step=1
    )

    refund_amount = st.number_input(
        "Refund Amount (₹)",
        min_value=0.0,
        value=300.0,
        step=50.0
    )

with right:

    return_reason = st.selectbox(
        "Return Reason",
        [
            "Changed mind",
            "Wrong item",
            "Defective",
            "Not as described",
            "Unknown"
        ]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Credit Card",
            "Debit Card",
            "UPI",
            "Net Banking",
            "Cash on Delivery"
        ]
    )

    days_to_return = st.number_input(
        "Days to Return",
        min_value=0,
        value=7,
        step=1
    )

    return_count = st.number_input(
        "Previous Return Count",
        min_value=0,
        value=1,
        step=1
    )

# ============================================================
# RISK CALCULATION
# ============================================================

if st.button(
    "🚨 Analyze Refund Request",
    use_container_width=True
):

    order_value = product_price * order_quantity

    if order_value > 0:

        refund_ratio = refund_amount / order_value

    else:

        refund_ratio = 0

    risk_score = 0

    risk_reasons = []

    # ----------------------------------------
    # HIGH REFUND RATIO
    # ----------------------------------------

    if refund_ratio >= 0.8:

        risk_score += 30

        risk_reasons.append(
            "High refund amount compared with order value"
        )

    elif refund_ratio >= 0.5:

        risk_score += 15

        risk_reasons.append(
            "Moderately high refund ratio"
        )

    # ----------------------------------------
    # FREQUENT RETURNS
    # ----------------------------------------

    if return_count >= 5:

        risk_score += 30

        risk_reasons.append(
            "High number of previous returns"
        )

    elif return_count >= 3:

        risk_score += 15

        risk_reasons.append(
            "Multiple previous returns"
        )

    # ----------------------------------------
    # QUICK RETURN
    # ----------------------------------------

    if days_to_return <= 2:

        risk_score += 10

        risk_reasons.append(
            "Very quick return after purchase"
        )

    # ----------------------------------------
    # RETURN REASON
    # ----------------------------------------

    if return_reason in [
        "Defective",
        "Wrong item",
        "Not as described"
    ]:

        risk_score += 10

        risk_reasons.append(
            "Return reason requires additional verification"
        )

    # ----------------------------------------
    # CAP SCORE
    # ----------------------------------------

    if risk_score > 100:

        risk_score = 100

    # ========================================================
    # DISPLAY RISK
    # ========================================================

    st.divider()

    st.subheader("📊 Fraud Risk Result")

    result_col1, result_col2, result_col3 = st.columns(3)

    result_col1.metric(
        "Order Value",
        f"₹{order_value:,.2f}"
    )

    result_col2.metric(
        "Refund Ratio",
        f"{refund_ratio:.2%}"
    )

    result_col3.metric(
        "Risk Score",
        f"{risk_score}/100"
    )

    # ========================================================
    # RISK STATUS
    # ========================================================

    if risk_score >= 60:

        st.error(
            "🚨 HIGH RISK\n\n"
            "This refund request appears suspicious."
        )

        status = "HIGH RISK"

    elif risk_score >= 30:

        st.warning(
            "⚠️ MEDIUM RISK\n\n"
            "This refund request requires manual review."
        )

        status = "MEDIUM RISK"

    else:

        st.success(
            "✅ LOW RISK\n\n"
            "Refund request appears legitimate."
        )

        status = "LOW RISK"

    # ========================================================
    # REASONS
    # ========================================================

    st.subheader("🔎 Risk Factors")

    if risk_reasons:

        for reason in risk_reasons:

            st.write(
                f"• {reason}"
            )

    else:

        st.write(
            "✅ No major suspicious patterns detected."
        )

    # ========================================================
    # TRANSACTION RESULT
    # ========================================================

    st.subheader("🧾 Transaction Decision")

    decision_df = pd.DataFrame({
        "Field": [
            "User ID",
            "Order ID",
            "Order Value",
            "Refund Amount",
            "Refund Ratio",
            "Return Count",
            "Days to Return",
            "Risk Score",
            "Risk Status"
        ],
        "Value": [
            user_id,
            order_id,
            f"₹{order_value:,.2f}",
            f"₹{refund_amount:,.2f}",
            f"{refund_ratio:.2%}",
            return_count,
            days_to_return,
            f"{risk_score}/100",
            status
        ]
    })

    st.dataframe(
        decision_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# HISTORICAL ANALYTICS
# ============================================================

st.divider()

st.header("📈 Historical Analytics")

analytics_col1, analytics_col2 = st.columns(2)

with analytics_col1:

    st.subheader("Order Value Distribution")

    if "order_value" in df.columns:

        st.bar_chart(
            df["order_value"].head(50)
        )

with analytics_col2:

    st.subheader("Refund Amount Distribution")

    if "refund_amount" in df.columns:

        st.bar_chart(
            df["refund_amount"].head(50)
        )

# ============================================================
# RETURN REASON ANALYSIS
# ============================================================

if "return_reason" in df.columns:

    st.divider()

    st.header("📦 Return Reason Analysis")

    reason_counts = (
        df["return_reason"]
        .fillna("Unknown")
        .value_counts()
    )

    st.bar_chart(
        reason_counts
    )

# ============================================================
# PAYMENT METHOD ANALYSIS
# ============================================================

if "payment_method" in df.columns:

    st.divider()

    st.header("💳 Payment Method Analysis")

    payment_counts = (
        df["payment_method"]
        .fillna("Unknown")
        .value_counts()
    )

    st.bar_chart(
        payment_counts
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Return & Refund Fraud Analytics | "
    "Machine Learning & Risk Analysis Project"
)
