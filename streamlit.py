from time import strftime
import streamlit as st
import pandas as pd
from gsheetsdb import connect

st.set_page_config(page_title="PrizePicks Odds", page_icon=":moneybag:", layout='wide')

conn = connect()

# Uses st.cache to only rerun when the query changes or after 3 min.
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
FAQs = st.container()

with header:
    st.title("PrizePicks Comparison Tool")
    st.subheader("Quick Summary")
    st.markdown("PrizePicks has countless sports picks playing at a given time. Lots of those picks are being offered on other sportsbooks, and you can use that to your advantage.\
        Every play on PrizePicks is *assumed to be 50/50,* but that's unlikely for every line. You can go to a sportsbook *(Draftkings in this case)* and play the odds.\
        **This tool finds plays with the same line on PrizePicks and Draftkings and displays them in the table below.**")
    st.markdown("*For example, Lionel Messi at 2 Shots is being offered on PrizePicks as an over/under, but on Draftkings, the over is -150 (60%). This is **not** a 50/50 play, there is a favor towards the over.*")
def highlight(s):
    is_plus = s == 'Under +'
    return ['background-color: #A4DFFF' if v else '' for v in is_plus]

def highlight2(s):
    is_plus = s == 'Over +'
    return ['background-color: #A4DFFF' if v else '' for v in is_plus]

with dataset:
    st.markdown("""---""")
    df = pd.DataFrame(rows)
    df.columns = ['Player', 'Team', 'Sport', 'Stat Type', 'Last Updated', 'Line','Over', 'Under', 'Probability', 'Favor']
    
   #df = pd.read_csv("MAIN_TABLE.csv")
    sports = st.multiselect('Filter by Sport', df['Sport'].unique(), default=df['Sport'].unique())
    ss_mode = st.checkbox('Screenshot Mode', value=False, help="Removes useless columns")
    filtered_df = df[df["Sport"].isin(sports)]
    if ss_mode:
        filtered_df = filtered_df.drop(['Last Updated', 'Sport', 'Team'], axis=1)
#     # st.dataframe(filtered_df.style.highlight_quantile(axis=0, subset='Probability (%)', color='SpringGreen', q_right=1, q_left=0.8)\
#     # .format({"Line": "{:.1f}", "Probability (%)": "{:.1f}"})\
#     # .apply(highlight)\
#     # .apply(highlight2))
    st.dataframe(filtered_df.style.highlight_quantile(axis=0, subset='Probability', color='#48F084', q_right=1, q_left=0.8)\
    .format({"Line": "{:.1f}","Over":"{0:+g}", "Under":"{0:+g}", "Probability": "{:.1f}%", "Last Updated": lambda x: "{}".format(x.strftime("%m/%d/%y %H:%M"))})\
    .apply(highlight)\
    .apply(highlight2), use_container_width=True)

    st.markdown("""
        <style>
        .small-font {
            font-size:13px !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<p class="small-font">Updates every 15 minutes. Refresh to update.</p>', unsafe_allow_html=True)

with FAQs:
    st.markdown("""---""")
    st.subheader("FAQs")
    with st.expander("Is this tool free?"):
        st.markdown("Yes. While similar tools can cost around \$15-\$50/Month, this tool will remain completely free. :smile:")
    with st.expander("The table is too small. How do I make it larger?"):
        st.markdown("**Option 1:** Hover over the table until a icon with two diagonal arrows appears. Click that and the table will take up your whole screen.")
        st.markdown("**Option 2:** Click the menu icon on the top right *(3 Vertical lines)*. Then click Settings -> Wide Mode.")
    with st.expander("What do the blue highlights mean?"):
        st.markdown('You may notice that there are rows in the *Favor* column that say *"Under +"* or *"Over +"*.\
            This means there is a **Favored Line** and an additonal edge for this play.')
        st.markdown("*For example, Steph Curry at 28.5 points is being offered on PrizePicks, but on Draftkings, the over is -135 (57%)\
            **and** the line is 31 points. The odds are **actually better than they appear** because of the better line on PrizePicks.*")
    with st.expander("What sports are supported?"):
        st.markdown("Sports currently supported: **NFL, NHL, NBA, & MLB.**")