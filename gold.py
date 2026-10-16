import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "b890f0cb7148263128658531fd7892f5"

rows=[]

end = datetime.today()

# Split into 5-day batches
for start_offset in range(0,30,5):

    end_date = end - timedelta(days=start_offset)

    start_date = end_date - timedelta(days=4)

    url = (
        f"https://api.metalpriceapi.com/v1/timeframe"
        f"?api_key={API_KEY}"
        f"&start_date={start_date.strftime('%Y-%m-%d')}"
        f"&end_date={end_date.strftime('%Y-%m-%d')}"
        f"&base=USD"
        f"&currencies=XAU"
    )

    print(url)

    response = requests.get(
        url,
        timeout=30
    )

    data = response.json()

    if data.get("success"):

        for date, value in data["rates"].items():

            rows.append({

                "Date": date,

                "Gold_Rate":
                value["XAU"]

            })

df = pd.DataFrame(rows)

df["Date"] = pd.to_datetime(
    df["Date"]
)

df = (
    df
    .drop_duplicates(
        subset=["Date"]
    )
    .sort_values(
        by="Date"
    )
)

# Convert Gold Rate → USD Price
# Convert Gold Rate → USD Price
# Convert Gold Rate → USD Price (1 Troy Ounce)
df["Gold_Price_USD"] = (
    1 /
    df["Gold_Rate"]
)

# USD → INR
USD_TO_INR = 86

df["Gold_Price_INR"] = (
    df["Gold_Price_USD"]
    *
    USD_TO_INR
)

# Convert Ounce → 1 Gram Gold Price
df["Gold_1Gram_INR"] = (
    df["Gold_Price_INR"]
    /
    31.1035
).round(2)
df.to_csv(
    "gold_last_30days.csv",
    index=False
)

print(df)