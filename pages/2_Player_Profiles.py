import streamlit as st
import pandas as pd  
import json
import wikipediaapi
from utilities import batting_stats, bowling_stats


st.set_page_config(
    page_title="Player Profiles",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="expanded",
)

def load_player_achievement():
    player_achivement = pd.read_csv('resources/players_achivements.csv')
    return player_achivement

def loading_data():
    batting_players_odi, batting_players_t20 = batting_stats.load_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.load_bowling_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.set_column_names(bowling_players_odi, bowling_players_t20)
    bowling_players_odi, bowling_players_t20 = bowling_stats.fill_null_values(bowling_players_odi, bowling_players_t20)
    player_info = pd.read_csv("resources/players_info.csv")
    return batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, player_info

def get_wikipedia_summary(player_name):
    wiki_wiki = wikipediaapi.Wikipedia('en', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    page = wiki_wiki.page(player_name)
    if page.exists():
        return page.summary
    else:
        return "Summary not available."


def get_wikipedia_summary(player_name):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(player_name)
    if page.exists():
        return page.summary.split('\n\n')[0]
    else:
        return "No Wikipedia page found for this player."
    
def display_player_info(player_info_row, batting_stats_odi, batting_stats_t20, bowling_stats_odi, bowling_stats_t20, player_achievement=None, player_caps=None):
    
    total_runs = int(batting_stats_odi.get('Runs', 0)) + int(batting_stats_t20.get('Runs', 0))
    total_wickets = int(bowling_stats_odi.get('Wickets Taken', 0)) + int(bowling_stats_t20.get('Wickets Taken', 0))
    
    with st.container(border=True):
        st.markdown(f'<h2 style="text-align: center; color: #F9694B;">{player_info_row["Full name"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<hr style="border-top: 2px solid #EF7D65;">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])  
        
        with col1:
            st.image(player_info_row['Photo'], width=320)
        
        with col2:
            st.markdown(f" **Age:** {player_info_row.get('Age', 'Unknown')}  \n")
            st.markdown(f" **Batting Style:** {player_info_row.get('Batting Style', '')}  \n")
            st.markdown(f" **Bowling Style:** {player_info_row.get('Bowling Style', '')}  \n")
            st.markdown(f" **Playing Order:** {player_info_row.get('Playing Order', '')}  \n")
            st.markdown(f" **District:** {player_info_row.get('District', '')}  \n")
            st.markdown(f" **Total Runs:** {total_runs}  \n")
            st.markdown(f" **Total Wickets Taken:** {total_wickets} ")
            
            if not pd.isna(player_caps):
                st.markdown(f" **International Caps:** {int(player_caps)}  \n")

            if player_achievement:
                st.markdown(f" **Achievement:** {player_achievement}  \n")
            
        with st.expander("Player Bio"):
            player_name = player_info_row["Full name"]
            # summary = get_wikipedia_summary(player_name)
            # st.write(summary)
            st.write('Player bio is being added soon. Stay tuned.😉')





def main():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20, player_info = loading_data()
    player_achievement = load_player_achievement()

    player_info = player_info.merge(player_achievement[['player_name', 'international_caps']], left_on='Name', right_on='player_name', how='left')

    player_info_sorted = player_info.sort_values(by='international_caps', ascending=False)
    st.markdown('<h1 style="text-align: center; color: red;">Meet the Players: Profiles</h1>', unsafe_allow_html=True)
    for _, player_row in player_info_sorted.iterrows():
        player_name = player_row['Name']
        
        caps = player_row['international_caps']
        achievement = None 
        player_achievement_row = player_achievement[player_achievement['player_name'] == player_name]
        if not player_achievement_row.empty:
            achievement = player_achievement_row.iloc[0]['achievement']

        # Retrieve batting and bowling stats
        batting_stats_odi = batting_players_odi[batting_players_odi['Player'] == player_name].iloc[0] if not batting_players_odi[batting_players_odi['Player'] == player_name].empty else {'Runs': 0}
        batting_stats_t20 = batting_players_t20[batting_players_t20['Player'] == player_name].iloc[0] if not batting_players_t20[batting_players_t20['Player'] == player_name].empty else {'Runs': 0}
        bowling_stats_odi = bowling_players_odi[bowling_players_odi['Player'] == player_name].iloc[0] if not bowling_players_odi[bowling_players_odi['Player'] == player_name].empty else {'Wickets Taken': 0}
        bowling_stats_t20 = bowling_players_t20[bowling_players_t20['Player'] == player_name].iloc[0] if not bowling_players_t20[bowling_players_t20['Player'] == player_name].empty else {'Wickets Taken': 0}

        # Display player profile
        display_player_info(player_row, batting_stats_odi, batting_stats_t20, bowling_stats_odi, bowling_stats_t20, achievement, caps)
        st.markdown('<hr>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()


