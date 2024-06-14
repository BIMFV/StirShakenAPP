import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

from pymongo import MongoClient

st.write("Stir Shaken report")


# MongoDB connection URI with authentication
uri = "mongodb://mfvilla:asGozuIW4rbdt@localhost:27017/dbanalytics_test"

# Establish connection
client = MongoClient(uri)

# Access the desired database
db = client['dbanalytics_test']

cursor= db.StirShaken_groups.find()

data = list(cursor)
df = pd.DataFrame(data)
df=df[['Week','ClientName','empty','numbers','short_number','Total']]

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters", key="unique_key_for_add_filters_checkbox")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

dff=pd.DataFrame(filter_dataframe(df))
st.dataframe(dff)



def create_bar_chart(df, column_name, chart_title):
    if column_name in df.columns:
        alphanumeric = df[['ClientName', column_name]]
        top_20_alphanumeric = alphanumeric.sort_values(by=column_name, ascending=False)
        top_20_alphanumeric = top_20_alphanumeric.head(20) if len(top_20_alphanumeric) >= 20 else top_20_alphanumeric

        fig = px.bar(
            x=top_20_alphanumeric['ClientName'],
            y=top_20_alphanumeric[column_name],
            labels={'x': 'Client Name', 'y': 'Count'},
            title=chart_title
        )
        fig.update_xaxes(tickangle=90, tickfont=dict(size=8))

        st.plotly_chart(fig)
    else:
        st.write(f"There are no {column_name} in this week.")

create_bar_chart(dff, 'numbers', 'Top 20 Clients numeric')
create_bar_chart(dff, 'empty', 'Top 20 Clients empty')
create_bar_chart(dff, 'short_number', 'Top 20 Clients short_number')
create_bar_chart(dff, 'spaces', 'Top 20 Clients spaces')
create_bar_chart(dff, 'letters', 'Top 20 Clients letters')


csv_data = dff.to_csv(index=False)

# Now use the download_button function with the CSV data
btn = st.download_button(
    label='Download CSV',
    data=csv_data,
    file_name='file.csv',
    mime='text/csv'
)

cursors= db.StirShaken_samples.find()

datas = list(cursors)
dfs = pd.DataFrame(datas)
csv_datas = dfs.to_csv(index=False)

btns = st.download_button(
    label='Download CSV CDR samples',
    data=csv_datas,
    file_name='Samples.csv',
    mime='text/csv'
)