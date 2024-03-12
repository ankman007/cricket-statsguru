import streamlit as st
from utilities import BattingStats, BowlingStats
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Comparison Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",

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
        select_match_type = st.selectbox("Select Match Type", match_type_options , key = "match_type")
        select_rating_type = st.selectbox("Choose Rating Type", rating_type_options , key= "rating_type")
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


def create_selectbox(series_1 , series_2):
    #creating columns for the selectboxes 
    column_1  , column_3 = st.columns(2)
    with column_1: 
        player_1 = st.selectbox(
            "Select a player" , 
            BowlingStats.my_union(series_1["Player"], series_2["Player"]) , 
            key="Player_1"
            )
    # with column_2:
    #     st.header("🆚")
    with column_3:
        
        player_2 = st.selectbox(
            "Select a player" , 
            BowlingStats.my_union(series_1["Player"], series_2["Player"]) , 
            key="Player_2")
@st.cache_data
def loading_info_data():
    df = pd.read_csv("resources/PlayersInfo.csv")
    return df       
def showing_info():
    data = loading_info_data()
    column1 , column2 = st.columns(2)
    with column1: 
        st.image(data[data['Name'] == st.session_state.Player_1]['Photo'].iloc[0] , width=250)
        st.markdown(f" **Age:** {int(data[data['Name'] == st.session_state.Player_1]['Age'].iloc[0])}")
        st.markdown(f" **Batting Style:** {data[data['Name'] == st.session_state.Player_1]['Batting Style'].iloc[0]}")
        st.markdown(f" **Bowling Style:** {data[data['Name'] == st.session_state.Player_1]['Bowling Style'].iloc[0]}")
        st.markdown(f" **Playing Order:** {data[data['Name'] == st.session_state.Player_1]['Playing Order'].iloc[0]}")
    with column2:
        st.image(data[data['Name'] == st.session_state.Player_2]['Photo'].iloc[0] , width = 250)
        st.markdown(f" **Age:** {int(data[data['Name'] == st.session_state.Player_2]['Age'].iloc[0])}")
        st.markdown(f" **Batting Style:** {data[data['Name'] == st.session_state.Player_2]['Batting Style'].iloc[0]}")
        st.markdown(f" **Bowling Style:** {data[data['Name'] == st.session_state.Player_2]['Bowling Style'].iloc[0]}")
        st.markdown(f" **Playing Order:** {data[data['Name'] == st.session_state.Player_2]['Playing Order'].iloc[0]}")


#creating pie charts for respective stats



  
def showing_data(batting_players_odi , bowling_players_odi , batting_players_t20 , bowling_players_t20):
    column1 , column2 , column3 , column4 = st.columns(4)
    with column1:
        selected_data = batting_players_odi[(batting_players_odi["Player"] == st.session_state.Player_1) | (batting_players_odi["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)

    with column2:
        selected_data = bowling_players_odi[(bowling_players_odi["Player"] == st.session_state.Player_1) | (bowling_players_odi["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)
    with column3:
        selected_data = batting_players_t20[(batting_players_t20["Player"] == st.session_state.Player_1) | (batting_players_t20["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)
    with column4:
        selected_data = bowling_players_t20[(bowling_players_t20["Player"] == st.session_state.Player_1) | (bowling_players_t20["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)


def one_on_one_comparision():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 = load_cricket_data()
    create_selectbox(batting_players_odi , batting_players_t20)
    showing_info()
    showing_data(batting_players_odi , bowling_players_odi , batting_players_t20 , bowling_players_t20)
        

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
