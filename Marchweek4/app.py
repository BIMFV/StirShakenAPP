import streamlit as st
import pandas as pd
import plotly.express as px

st.write("Stir Shaken report")

df=pd.read_excel(r'/home/mfvilla/projects/StirShaken/Marchweek4/Customer_by_SrcNumberRoute_pt.xlsx')
st.dataframe(df, use_container_width=True)

if 'numbers' in df.columns:
    alphanumeric = df[['ClientName', 'numbers']]
    top_20_alphanumeric = alphanumeric.sort_values(by='numbers', ascending=False)

    # Limit to top 20 rows, but include all unique client names
    top_20_alphanumeric = top_20_alphanumeric.head(20) if len(top_20_alphanumeric) >= 20 else top_20_alphanumeric

    fig = px.bar(
        x=top_20_alphanumeric['ClientName'],
        y=top_20_alphanumeric['numbers'],
        labels={'x': 'Client Name', 'y': 'Count'},
        title='Top 20 Clients numeric'
    )
    fig.update_xaxes(tickangle=90, tickfont=dict(size=8))  # Rotate labels and adjust font size

    # Save the plotly figure as HTML
    fig.write_html('top_20_clients_numeric.html')

    # Display the figure in Streamlit
    st.plotly_chart(fig)

else:
    st.write("There are no numeric ANI in this week.")


if 'empty' in df.columns:
    alphanumeric = df[['ClientName', 'empty']]
    top_20_alphanumeric = alphanumeric.sort_values(by='empty', ascending=False)

    # Limit to top 20 rows, but include all unique client names
    top_20_alphanumeric = top_20_alphanumeric.head(20) if len(top_20_alphanumeric) >= 20 else top_20_alphanumeric

    fig = px.bar(
        x=top_20_alphanumeric['ClientName'],
        y=top_20_alphanumeric['empty'],
        labels={'x': 'Client Name', 'y': 'Count'},
        title='Top 20 Clients empty'
    )
    fig.update_xaxes(tickangle=90, tickfont=dict(size=8))  # Rotate labels and adjust font size

    # Save the plotly figure as HTML
    fig.write_html('top_20_clients_empty.html')

    # Display the figure in Streamlit
    st.plotly_chart(fig)

else:
    st.write("There are no empty ANI in this week.")


if 'short_number' in df.columns:
    alphanumeric = df[['ClientName', 'short_number']]
    top_20_alphanumeric = alphanumeric.sort_values(by='short_number', ascending=False)

    # Limit to top 20 rows, but include all unique client names
    top_20_alphanumeric = top_20_alphanumeric.head(20) if len(top_20_alphanumeric) >= 20 else top_20_alphanumeric

    fig = px.bar(
        x=top_20_alphanumeric['ClientName'],
        y=top_20_alphanumeric['short_number'],
        labels={'x': 'Client Name', 'y': 'Count'},
        title='Top 20 Clients short_number'
    )
    fig.update_xaxes(tickangle=90, tickfont=dict(size=8))  # Rotate labels and adjust font size

    # Save the plotly figure as HTML
    fig.write_html('top_20_clients_short_number.html')

    # Display the figure in Streamlit
    st.plotly_chart(fig)

else:
    st.write("There are no short number ANI in this week.")

if 'spaces' in df.columns:
    alphanumeric = df[['ClientName', 'spaces']]
    top_20_alphanumeric = alphanumeric.sort_values(by='spaces', ascending=False)

    # Limit to top 20 rows, but include all unique client names
    top_20_alphanumeric = top_20_alphanumeric.head(20) if len(top_20_alphanumeric) >= 20 else top_20_alphanumeric

    fig = px.bar(
        x=top_20_alphanumeric['ClientName'],
        y=top_20_alphanumeric['spaces'],
        labels={'x': 'Client Name', 'y': 'Count'},
        title='Top 20 Clients spaces'
    )
    fig.update_xaxes(tickangle=90, tickfont=dict(size=8))  # Rotate labels and adjust font size

    # Save the plotly figure as HTML
    fig.write_html('top_20_clients_spaces.html')

    # Display the figure in Streamlit
    st.plotly_chart(fig)

else:
    st.write("There are no spaces in ANI in this week.")

if 'letters' in df.columns:
    alphanumeric = df[['ClientName', 'letters']]
    top_20_alphanumeric = alphanumeric.sort_values(by='letters', ascending=False)

    # Limit to top 20 rows, but include all unique client names
    top_20_alphanumeric = top_20_alphanumeric.head(20) if len(top_20_alphanumeric) >= 20 else top_20_alphanumeric

    fig = px.bar(
        x=top_20_alphanumeric['ClientName'],
        y=top_20_alphanumeric['letters'],
        labels={'x': 'Client Name', 'y': 'Count'},
        title='Top 20 Clients letters'
    )
    fig.update_xaxes(tickangle=90, tickfont=dict(size=8))  # Rotate labels and adjust font size

    # Save the plotly figure as HTML
    fig.write_html('top_20_clients_letters.html')

    # Display the figure in Streamlit
    st.plotly_chart(fig)

else:
    st.write("There are no letters type ANI in this week.")

df.to_csv('dftext.csv')
dft=pd.read_csv('dftext.csv')

with open('dftext.csv', "rb") as fp:
    btn=st.download_button('Download CSV',fp,'file.csv')


