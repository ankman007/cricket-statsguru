import streamlit as st
from utilities import multiplayer_comparison , one_on_one_comparison
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Comparison Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",

)
match_type_options = ["ODI", "T20"]  # Removed "Overall Statistics"
rating_type_options = ["Batting", "Bowling"]
default_players = ["K Bhurtel", "RK Paudel", 'Sompal Kami', 'S Bhari', 'Aasif Sheikh', 'KS Airee']
select_match_type = st.sidebar.selectbox("Select Match Type", match_type_options , key = "match_type")
select_rating_type = st.sidebar.selectbox("Choose Rating Type", rating_type_options , key= "rating_type")
def main():
    st.markdown("<h1 style='text-align: center; color: black;'>Compare Cricketers: Batting, Bowling, Head-to-Head Records & Statistics</h1>", unsafe_allow_html=True)

    tab_titles = [
        "One-on-One Comparison",
        "Multi-player Comparison",
    ]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        one_on_one_comparison.one_on_one_comparision()
    with tabs[1]:
        multiplayer_comparison.multi_player_comparison()

if __name__ == "__main__":
    main()
