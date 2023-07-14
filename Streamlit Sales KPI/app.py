import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import datetime

st.title("Sales Report")


@st.cache
def load_data():
    df = pd.read_parquet("s3://mega-lake/ProcessedData/Sales/sales_detail/mpr/2023/")
    df["so_create_date"] = pd.to_datetime(df["so_create_date"])
    return df


df = load_data()

# line Chart
fig = px.line(
    df.groupby(["so_create_date"], as_index=False)[["transaction_price"]].sum(),
    x="so_create_date",
    y="transaction_price",
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
fig.update_layout({"paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)"})
st.plotly_chart(fig, use_container_width=True)


# Metrics
sales_perday = df.groupby(["so_create_date", "monthnum"], as_index=False)[
    ["transaction_price"]
].sum()
month = str(datetime.datetime.now().month).zfill(2)
now = sales_perday[sales_perday["monthnum"] == month][-3:]["so_create_date"].unique()[0]
yesterday = sales_perday[sales_perday["monthnum"] == month][-4:][
    "so_create_date"
].unique()[0]

delta = round(
    (
        (
            sales_perday[sales_perday["so_create_date"] == now][
                "transaction_price"
            ].sum()
            / sales_perday[sales_perday["so_create_date"] == yesterday][
                "transaction_price"
            ].sum()
        )
        - 1
    )
    * 100,
    3,
)


st.metric(
    label="Sales",
    value=f'Rp{sales_perday[sales_perday["so_create_date"] == now]["transaction_price"].sum():,.0f}',
    delta=f"{delta} %",
)


# st.line_chart(
#     df.groupby(["so_create_date"], as_index=False)[["transaction_price"]].sum(),
#     x="so_create_date",
#     y="transaction_price",
# )
