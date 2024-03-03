import streamlit as st 
import pandas as pd
import numpy as np
from DataProcessingModule import  clean_dataframe
import plotly.express as px

st.title("Batting Stats!")

#getting the data
batting_players_odi = pd.read_csv("data/batting_players_odi.csv")
batting_players_t20 = pd.read_csv("data/batting_players_t20.csv")

#cleaning the dataframe through the module 
clean_dataframe(batting_players_odi)
clean_dataframe(batting_players_t20)

#cleaning the Highest score columns 
batting_players_odi['HS'] = batting_players_odi['HS'].str.replace('*' , '' , regex=True)
batting_players_t20['HS'] = batting_players_t20['HS'].str.replace('*' , '' , regex=True)

#changing the data type of few columns 
str_column = ['Inns', 'NO', 'Runs', 'HS', 'Ave', 'SR', '100','50', '0']
batting_players_t20[str_column] = batting_players_t20[str_column].apply(pd.to_numeric, errors='coerce')
batting_players_odi[str_column] = batting_players_odi[str_column].apply(pd.to_numeric, errors='coerce')



#extracting players without repeating
def my_union(column_1 , column_2):
    column_1 = set(column_1)
    column_2 = set(column_2)
    return list(column_1.union(column_2))

#changing columns of the dataframes
columns = ['Player','Span','Matches' , 'Innings' , 'Not Outs' , 'Runs Scored' , 'Highest Score' , 'Batting Average' , 'Strike Rate' , 'Hundreds' , 'Fifties' , 'Ducks']
batting_players_t20.columns = columns 
batting_players_odi.columns = columns

#defining selectbox and sessions
series_type = st.selectbox(
    'Select Cricket Match Type' , 
    ('ODI' , 'T20') , 
    key = "Batting_Series"
)
stat_type = st.selectbox(
    'Select Stats of Players' , 
    columns[2:] , 
    key = "Batting_stats"
)
players = st.multiselect(
    'Select Players' , 
    my_union(batting_players_odi['Player'] , batting_players_t20['Player']) , 
    key = "Player_chosen"
)

 
if st.session_state.Batting_Series == 'ODI':
    if st.session_state.Batting_stats:
        if st.session_state.Player_chosen:
            #filtering players
            filtered_players = batting_players_odi[batting_players_odi['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Player': filtered_players['Player'] , 
                f'{st.session_state.Batting_stats}': filtered_players[st.session_state.Batting_stats]
            })
           
            st.bar_chart(chart_data.set_index('Player') , color="#f4a261")
            st.dataframe(chart_data.set_index('Player') , width= 800)



#Doing the same for T20 too!
if st.session_state.Batting_Series == 'T20':
    if st.session_state.Batting_stats:
        if st.session_state.Player_chosen:
            filtered_players = batting_players_t20[batting_players_t20['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Player': filtered_players['Player'] , 
                f'{st.session_state.Batting_stats}': filtered_players[st.session_state.Batting_stats]
            })
            st.bar_chart(chart_data.set_index('Player') , color="#f4a261")
            st.dataframe(chart_data.set_index('Player') , width= 800)

st.header("Some Noticeable Stats🏏")



   
    
