import pandas as pd

def load_and_clean_data():
    df = pd.read_csv("data/ecommerce_data.csv")

    df.dropna(inplace=True)

    df['payment_method'] = df['payment_method'].astype('category').cat.codes

    return df

if __name__ == "__main__":
    df = load_and_clean_data()
    print(df.head())
