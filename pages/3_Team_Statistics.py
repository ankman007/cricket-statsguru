import streamlit as st
from visulizations.BattingStats import display_batting_stats
from visulizations.BowlingStats import display_bowling_stats

st.set_page_config(
    page_title="Team Statistics",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)
def main():
    tab_titles = [
        "Batting Statistics",
        "Bowling Statistics",
    ]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        display_batting_stats()
    with tabs[1]:
        display_bowling_stats()

if __name__ == "__main__":
    main()

