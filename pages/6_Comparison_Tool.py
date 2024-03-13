import streamlit as st
from utilities import BattingStats, BowlingStats , multiplayerComp , oneOnonecomp
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Comparison Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",

)


def main():
    st.markdown("<h1 style='text-align: center; color: black;'>Compare Cricketers: Batting, Bowling, Head-to-Head Records & Statistics</h1>", unsafe_allow_html=True)

    tab_titles = [
        "One-on-One Comparison",
        "Multi-player Comparison",
    ]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        oneOnonecomp.one_on_one_comparision()
    with tabs[1]:
        multiplayerComp.multi_player_comparison()

if __name__ == "__main__":
    main()
