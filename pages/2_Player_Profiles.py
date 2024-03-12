import streamlit as st
from utilities import BattingStats , BowlingStats
import pandas as pd  

st.set_page_config(
    page_title="Player Profiles",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
    ### Welcome to the player profile!
""")

##Loading the data
def loading_data():
    batting_players_odi, batting_players_t20 = BattingStats.load_data()
    bowling_players_odi, bowling_players_t20 = BowlingStats.load_bowling_data()
    bowling_players_odi, bowling_players_t20 = BowlingStats.set_column_names(bowling_players_odi, bowling_players_t20)
    bowling_players_odi, bowling_players_t20 = BowlingStats.fill_null_values(bowling_players_odi, bowling_players_t20)
    player_info = pd.read_csv("resources/PlayersInfo.csv")
    return batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 , player_info

##showing data in columns
def show_data(batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 , player_info ):
    Players = player_info["Name"]
    for idx , i in enumerate(Players):
        main_container = st.container(border=True)
        main_container.markdown(f"### {player_info[player_info['Name'] == Players[idx]]['Full name'].iloc[0]}")
        column1 , column2 = st.columns(2)
        with column1: 
            main_container.image(player_info[player_info['Name'] == Players[idx]]['Photo'].iloc[0] , width=100)
        with column2:
            try: 
                age = int(player_info[player_info['Name'] == Players[idx]]['Age'].iloc[0])
            except:
                age = "Unknown"
            main_container.markdown(f" **Age:** {age}")
            main_container.markdown(f" **Batting Style:** {player_info[player_info['Name'] == Players[idx]]['Batting Style'].iloc[0]}")
            main_container.markdown(f" **Bowling Style:** {player_info[player_info['Name'] == Players[idx]]['Bowling Style'].iloc[0]}")
            main_container.markdown(f" **Playing Order:** {player_info[player_info['Name'] == Players[idx]]['Playing Order'].iloc[0]}")
            main_container.markdown(f" **District:** {player_info[player_info['Name'] == Players[idx]]['District'].iloc[0]}")
            try:
                main_container.markdown(f" **ODI Runs:** {int(batting_players_odi[batting_players_odi.Player == i]['Runs'].iloc[0])}")
            except:
                main_container.markdown(f" **ODI Runs:** {0}")
            try:
                main_container.markdown(f" **T20 Runs:** {int(batting_players_t20[batting_players_t20.Player == i]['Runs'].iloc[0])}")
            except:
                main_container.markdown(f" **T20 Runs:** {0}")
            try:
                main_container.markdown(f" **ODI Wickets:** {int(bowling_players_odi[bowling_players_odi.Player == i]['Wickets Taken'].iloc[0])}")
            except:
                main_container.markdown(f" **ODI Wickets:** {0}")
            try:
                main_container.markdown(f" **T20 Wickets:** {int(bowling_players_t20[bowling_players_t20.Player == i]['Wickets Taken'].iloc[0])}")
            except:
                main_container.markdown(f" **T20 Wickets:** {0}")
            
            
            # st.markdown(f" **T20 Runs:** {int(batting_players_t20[batting_players_t20.Player == i]['Runs'].iloc[0])}")


def main():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 , player_info = loading_data()
    show_data( batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 , player_info)


if __name__ == "__main__":
    main()