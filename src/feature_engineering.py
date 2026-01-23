import pandas as pd

def create_features(df):
    df['high_refund_flag'] = df['refund_amount'] > 500
    df['frequent_return_flag'] = df['return_count'] > 3
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/ecommerce_data.csv")
    df = create_features(df)
    print(df.head())
