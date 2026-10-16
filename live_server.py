
import requests
import pandas as pd
import os
from datetime import datetime
API_KEY = "949fdd98b040f543be4cedb61f7b3c61"

url = (
    f"https://api.metalpriceapi.com/v1/latest"
    f"?api_key={API_KEY}"
    f"&base=USD"
    f"&currencies=XAU"
)

response = requests.get(url)

data = response.json()

if data["success"]:

    now = datetime.now()

    new_row = pd.DataFrame([{
        "Date": now.strftime("%Y-%m-%d"),
        "Hour": now.strftime("%H:00"),
        "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "Gold_Rate": list(data["rates"].values())[0]
    }])

    file = "gold_hourly_7days.csv"

    if os.path.exists(file):

        old = pd.read_csv(file)

        df = pd.concat(
            [old, new_row],
            ignore_index=True
        )

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        keep_from = (
            datetime.now()
            - pd.Timedelta(days=6)
        )

        df = (
            df[df["Date"] >= keep_from]
            .drop_duplicates(
                subset=["Timestamp"]
            )
        )

    else:

        df = new_row

    df.to_csv(
        file,
        index=False
    )

    print(df.tail())

else:

    print(data["error"])