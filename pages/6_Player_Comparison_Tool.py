import streamlit as st 
import pandas as pd 
import plotly.express as px 
from visulizations import BattingStats , BowlingStats #Using the modules! Mainly for loading data

#Setting up page configurations
st.set_page_config(
    page_title="Player Comparison Tool",
    page_icon="🆚",
    layout="wide",
    initial_sidebar_state="collapsed",
)
#loading data
batting_players_odi  , batting_players_t20 = BattingStats.load_data()
bowling_players_odi, bowling_players_t20 = BowlingStats.load_bowling_data()
bowling_players_odi, bowling_players_t20 = BowlingStats.set_column_names(bowling_players_odi, bowling_players_t20)
bowling_players_odi, bowling_players_t20 = BowlingStats.fill_null_values(bowling_players_odi, bowling_players_t20)

def creatingSelectbox():
    column_1 , column_2 , column_3 = st.columns([4,1,4])
    with column_1:
        player_1  = st.selectbox(
            "Select a player" , 
            BowlingStats.my_union(batting_players_odi["Player"] , batting_players_t20["Player"]) , 
            key="player1" , 
            index = BowlingStats.my_union(batting_players_odi["Player"] , batting_players_t20["Player"]).index("K Bhurtel")
        )
    with column_2:
      st.markdown("# .VS")

    with column_3:
        player_2 = st.selectbox(
            "Select a player" , 
            BowlingStats.my_union(batting_players_odi["Player"] , batting_players_t20["Player"]) , 
            key="player2" , 
            index= BowlingStats.my_union(batting_players_odi["Player"] , batting_players_t20["Player"]).index("RK Paudel")
        )
   
def showing_Data(): #showing data through table
    column_1 , column_2 , column_3 , column_4 = st.columns(4)
    
    with column_1 :
        st.header("Batting ODI")
        st.markdown(f"{st.session_state.player1} vs {st.session_state.player2} ")
        df1 = batting_players_odi[(batting_players_odi["Player"] == st.session_state.player1) | (batting_players_odi['Player'] == st.session_state.player2)].set_index("Player").drop(["Span"] , axis = 1)
        st.dataframe(df1.T)

    with column_2 :
        st.header("Batting T20")
        st.markdown(f"{st.session_state.player1} vs {st.session_state.player2} ")
        df2 = batting_players_t20[(batting_players_t20["Player"] == st.session_state.player1) | (batting_players_t20['Player'] == st.session_state.player2)].set_index("Player").drop(["Span"] , axis = 1)
        st.dataframe(df2.T)

    with column_3 :
        st.header("Bowling ODI")
        st.markdown(f"{st.session_state.player1} vs {st.session_state.player2} ")
        df3 = bowling_players_odi[(bowling_players_odi["Player"] == st.session_state.player1) | (bowling_players_odi['Player'] == st.session_state.player2)].set_index("Player").drop(["Span" , "Best Inning Bowling"] , axis = 1)
        st.dataframe(df3.T)

    with column_4 :
        st.header("Bowling T20")
        st.markdown(f"{st.session_state.player1} vs {st.session_state.player2} ")
        df4 = bowling_players_t20[(bowling_players_t20["Player"] == st.session_state.player1) | (bowling_players_t20['Player'] == st.session_state.player2)].set_index("Player").drop(["Span" , "Best Inning Bowling"] , axis = 1)
        st.dataframe(df4.T)



#main code
def main():
    creatingSelectbox()
    showing_Data()

if __name__ == "__main__":
    main()