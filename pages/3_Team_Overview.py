import streamlit as st
from utilities.BattingStats import display_batting_stats
from utilities.BowlingStats import display_bowling_stats

st.set_page_config(
    page_title="Team Statistics",
    page_icon="📊",
    layout="centered",
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

# TO-DOs 
# Highest Scores of batting & bowling 
# Collect data of individual player
# Series Analysis, default values, top section to bottom 
# Find stories behind the data
# complete section for 3: player profile, tornament tracker, player comparision tool