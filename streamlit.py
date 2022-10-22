from time import strftime
import streamlit as st
import pandas as pd
from gsheetsdb import connect
import re
conn = connect()



Perform SQL query on the Google Sheet.
Uses st.cache to only rerun when the query changes or after 3 min.
@st.cache(ttl=180)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows



sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

header = st.container()
dataset = st.container()
filters = st.container()

with header:
    st.title("Prizepicks Line Comparison Tool")
    st.subheader("Quick Summary")
    st.markdown("Prizepicks has countless sports picks playing at a given time. And you don't need to know much about every sport to use this tool. Lots of the plays on Prizepicks are being offered on other sportsbooks, and we can use that to our advantage. You can go to a sportsbook (Draftkings in this case) and compare the odds. Every play on Prizepicks is **assumed to be 50/50**, but that's impossible for every line.")
    st.markdown("*For example, Lionel Messi at 2 Shots is being offered on Prizepicks as an over/under, but on Draftkings, the over is -150 (60%). This is **not** a 50/50 play, there is a favor towards the over.*")

def highlight(s):
    is_max = s == 'Under +'
    return ['background-color: PaleTurquoise' if v else '' for v in is_max]

def highlight2(s):
    is_max = s == 'Over +'
    return ['background-color: PaleTurquoise' if v else '' for v in is_max]

with dataset:
    df = pd.DataFrame(rows)

    #df = pd.read_csv("MAIN_TABLE.csv")
    df.columns = ['Player', 'Team', 'Sport', 'Stat Type', 'Last Updated', 'Line', 'Probability (%)', 'Favor']
    #df = df.style.highlight_quantile(axis=0, subset='Probability (%)', color='#97F589', q_right=1, q_left=0.8).format({"Line": "{:.1f}", "Probability (%)": "{:.1f}"})

    sports = st.multiselect('Filter by Sport', df['Sport'].unique(), default=df['Sport'].unique())

    filtered_df = df[df["Sport"].isin(sports)]
    # st.dataframe(filtered_df.style.highlight_quantile(axis=0, subset='Probability (%)', color='SpringGreen', q_right=1, q_left=0.8)\
    # .format({"Line": "{:.1f}", "Probability (%)": "{:.1f}"})\
    # .apply(highlight)\
    # .apply(highlight2))
    st.dataframe(filtered_df.style.highlight_quantile(axis=0, subset='Probability (%)', color='#97F589', q_right=1, q_left=0.8)\
    .format({"Line": "{:.1f}", "Probability (%)": "{:.1f}", "Last Updated": lambda x: "{}"\
    .format(x.strftime("%m/%d/%y %H:%M"))}\
    .apply(highlight)\
    .apply(highlight2)), use_container_width=True)
