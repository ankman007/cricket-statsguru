import streamlit as st
from utilities import BattingStats, BowlingStats

st.set_page_config(
    page_title="Comparison Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",

)

# Loading data
def load_cricket_data():
    batting_players_odi, batting_players_t20 = BattingStats.load_data()
    bowling_players_odi, bowling_players_t20 = BowlingStats.load_bowling_data()
    bowling_players_odi, bowling_players_t20 = BowlingStats.set_column_names(bowling_players_odi, bowling_players_t20)
    bowling_players_odi, bowling_players_t20 = BowlingStats.fill_null_values(bowling_players_odi, bowling_players_t20)
    return batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20

# Create user options
def user_options(player_options):
    match_type_options = ["ODI", "T20"]  # Removed "Overall Statistics"
    rating_type_options = ["Batting", "Bowling"]
    default_players = ["K Bhurtel", "RK Paudel", 'Sompal Kami', 'S Bhari', 'Aasif Sheikh', 'KS Airee']
    with st.sidebar: 
        select_match_type = st.selectbox("Select Match Type", match_type_options)
        select_rating_type = st.selectbox("Choose Rating Type", rating_type_options)
    select_players = st.multiselect("Select Players To Compare", player_options, default_players, key="players")

    return select_players, select_match_type, select_rating_type

def player_overview():
    st.markdown(f"<h3>Basic Overview</h3>", unsafe_allow_html=True)
    st.write("contains age, batting style, bowling style, district, playing role & so on")

# Display batting and bowling stats for selected players
def show_data(batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, selected_players, match_type, rating_type):

    st.markdown(f"<h3>{rating_type} Statistics Comparision Between Players In {match_type} Matches</h3>", unsafe_allow_html=True)

    df = batting_players_odi if rating_type == 'Batting' else bowling_players_odi
    df = df if match_type == 'ODI' else (batting_players_t20 if rating_type == 'Batting' else bowling_players_t20)

    stats_df = df[df["Player"].isin(selected_players)].set_index("Player").drop(["Span", "Best Inning Bowling"] if rating_type == 'Bowling' else ["Span"], axis=1)
    stats_df = stats_df.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)
    st.write(stats_df.T)

def multi_player_comparison():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 = load_cricket_data()
    player_options = BowlingStats.my_union(batting_players_odi["Player"], batting_players_t20["Player"])
    selected_players, match_type, rating_type = user_options(player_options)

    if selected_players:
        player_overview()
        show_data(batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, selected_players, match_type, rating_type)

def one_on_one_comparision():
    pass

def main():
    st.markdown("<h1 style='text-align: center; color: black;'>Compare Cricketers: Batting, Bowling, Head-to-Head Records & Statistics</h1>", unsafe_allow_html=True)

    tab_titles = [
        "One-on-One Comparison",
        "Multi-player Comparison",
    ]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        one_on_one_comparision()
    with tabs[1]:
        multi_player_comparison()

if __name__ == "__main__":
    main()
