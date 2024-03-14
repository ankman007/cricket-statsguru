import streamlit as st
import pandas as pd  
from utilities import batting_stats, bowling_stats


st.set_page_config(
    page_title="Player Profiles",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="expanded",
)

def loading_data():
    batting_players_odi, batting_players_t20 = batting_stats.load_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.load_bowling_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.set_column_names(bowling_players_odi, bowling_players_t20)
    bowling_players_odi, bowling_players_t20 = bowling_stats.fill_null_values(bowling_players_odi, bowling_players_t20)
    player_info = pd.read_csv("resources/players_info.csv")
    return batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, player_info

def display_player_info(player_info_row, batting_stats_odi, batting_stats_t20, bowling_stats_odi, bowling_stats_t20):
    
    total_runs = batting_stats_odi.get('Runs', 0) + batting_stats_t20.get('Runs', 0)
    total_wickets = bowling_stats_odi.get('Wickets Taken', 0) + bowling_stats_t20.get('Wickets Taken', 0)
    
    with st.container(border=True):
        # st.markdown(f"### {player_info_row['Full name']}", unsafe_allow_html=True)
        st.markdown(f'<h2 style="text-align: center; color: #F9694B;">{player_info_row["Full name"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<hr style="border-top: 2px solid #EF7D65;">', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])  
        
        with col1:
            st.image(player_info_row['Photo'], width=250)
        
        with col2:
            st.markdown(f" **Age:** {player_info_row.get('Age', 'Unknown')}  \n"
                        f" **Batting Style:** {player_info_row.get('Batting Style', '')}  \n"
                        f" **Bowling Style:** {player_info_row.get('Bowling Style', '')}  \n"
                        f" **Playing Order:** {player_info_row.get('Playing Order', '')}  \n"
                        f" **District:** {player_info_row.get('District', '')}  \n"
                        f" **Total Runs:** {total_runs}  \n"
                        f" **Total Wickets Taken:** {total_wickets}  \n")
        with st.expander("Player Bio"):
            st.write('Player bio is being added soon. Stay tuned.😉')

def main():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, player_info = loading_data()
    
    for _, player_row in player_info.iterrows():
        player_name = player_row['Name']
        
        if not batting_players_odi[batting_players_odi['Player'] == player_name].empty:
            batting_stats_odi = batting_players_odi[batting_players_odi['Player'] == player_name].iloc[0]
        else:
            batting_stats_odi = {'Runs': 0}  
        
        if not batting_players_t20[batting_players_t20['Player'] == player_name].empty:
            batting_stats_t20 = batting_players_t20[batting_players_t20['Player'] == player_name].iloc[0]
        else:
            batting_stats_t20 = {'Runs': 0}  
        
        if not bowling_players_odi[bowling_players_odi['Player'] == player_name].empty:
            bowling_stats_odi = bowling_players_odi[bowling_players_odi['Player'] == player_name].iloc[0]
        else:
            bowling_stats_odi = {'Wickets Taken': 0}  
        
        if not bowling_players_t20[bowling_players_t20['Player'] == player_name].empty:
            bowling_stats_t20 = bowling_players_t20[bowling_players_t20['Player'] == player_name].iloc[0]
        else:
            bowling_stats_t20 = {'Wickets Taken': 0}  
        
        display_player_info(player_row, batting_stats_odi, batting_stats_t20, bowling_stats_odi, bowling_stats_t20)

if __name__ == "__main__":
    main()


