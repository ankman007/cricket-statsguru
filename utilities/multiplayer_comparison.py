import streamlit as st
from utilities import batting_stats, bowling_stats 
import pandas as pd
import plotly.express as px

@st.cache_data
def loading_player_info():
    df = pd.read_csv("resources/players_info.csv")
    return df   

# Loading data
def load_cricket_data():
    batting_players_odi, batting_players_t20 = batting_stats.load_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.load_bowling_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.set_column_names(bowling_players_odi, bowling_players_t20)
    bowling_players_odi, bowling_players_t20 = bowling_stats.fill_null_values(bowling_players_odi, bowling_players_t20)
    return batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20


def user_options(player_options):
    match_type_options = ["ODI", "T20"]  
    rating_type_options = ["Batting", "Bowling"]
    default_players = ["K Bhurtel", "RK Paudel", 'Sompal Kami', 'S Bhari', 'Aasif Sheikh', 'KS Airee']
    
    select_players = st.multiselect("Select Players To Compare", player_options, default_players, key="players")
    return select_players


def player_overview(selected_players):
    st.markdown(f"<h3>Basic Overview</h3>", unsafe_allow_html=True)
    player_info = loading_player_info()
    selected_players_data = player_info[player_info['Name'].isin(selected_players)]
    selected_players_data = selected_players_data.drop(columns='Photo')     
    selected_players_data['Age'] = selected_players_data['Age'].astype(int)

    html_table = selected_players_data.to_html(bold_rows=True, index=False, classes=["styled-table"], justify='left')
    st.markdown(html_table, unsafe_allow_html=True)


def show_data(batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, selected_players, match_type, rating_type):
    st.markdown(f"<h3>{rating_type} Statistics Comparision Between Players In {match_type} Matches</h3>", unsafe_allow_html=True)
    df = batting_players_odi if rating_type == 'Batting' else bowling_players_odi
    df = df if match_type == 'ODI' else (batting_players_t20 if rating_type == 'Batting' else bowling_players_t20)

    stats_df = df[df["Player"].isin(selected_players)].set_index("Player").drop(["Span", "Best Inning Bowling"] if rating_type == 'Bowling' else ["Span"], axis=1)

    stats_df = stats_df.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)
    stats_df_transposed = stats_df.T

    html_table = stats_df_transposed.to_html(index=True, bold_rows=True, classes=["styled-table"], border=0, justify="left")
    st.markdown(html_table, unsafe_allow_html=True)

def multi_player_comparison():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 = load_cricket_data()
    player_options = bowling_stats.my_union(batting_players_odi["Player"], batting_players_t20["Player"])
    selected_players= user_options(player_options)
    match_type = st.session_state.match_type
    rating_type = st.session_state.rating_type

    if selected_players:
        player_overview(selected_players)
        st.markdown("<hr>", unsafe_allow_html=True)
        show_data(batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, selected_players, match_type, rating_type)