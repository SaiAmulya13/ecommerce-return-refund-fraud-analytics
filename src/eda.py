import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/ecommerce_data.csv")

sns.countplot(x="fraud_label", data=df)
plt.title("Fraud vs Legit Transactions")
plt.show()

sns.boxplot(x="fraud_label", y="refund_amount", data=df)
plt.title("Refund Amount vs Fraud")
plt.show()
