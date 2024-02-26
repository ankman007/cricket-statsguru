import streamlit as st 
import pandas as pd
import numpy as np
from DataProcessingModule import  clean_dataframe

#extracting the numerical values only!!
def changing_to_float(df, column):
    try:
        return pd.to_numeric(df[column].str.replace('*' , '' , regex = False), errors='coerce').astype(float).squeeze()
    except:
        return df[column]

st.title("Hello!")
st.header("Welcome to the the batting section of Nepali Players!")

#getting the data
batting_players_odi = pd.read_csv("data/batting_players_odi.csv")
batting_players_t20 = pd.read_csv("data/batting_players_t20.csv")

#cleaning the dataframe through the module 
clean_dataframe(batting_players_odi)
clean_dataframe(batting_players_t20)

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
    batting_players_t20['Player'] , 
    key = "Player_chosen"
)

 
if st.session_state.Batting_Series == 'ODI':
    if st.session_state.Batting_stats:
        if st.session_state.Player_chosen:
            #filtering players
            filtered_players = batting_players_odi[batting_players_odi['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Players': filtered_players['Player'] , 
                f'{st.session_state.Batting_stats}': changing_to_float(filtered_players , st.session_state.Batting_stats)
            })
            st.bar_chart(chart_data.set_index('Players') , color="#f4a261")



#Doing the same for T20 too!
if st.session_state.Batting_Series == 'T20':
    if st.session_state.Batting_stats:
        if st.session_state.Player_chosen:
            filtered_players = batting_players_t20[batting_players_t20['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Players': filtered_players['Player'] , 
                f'{st.session_state.Batting_stats}': changing_to_float(filtered_players , st.session_state.Batting_stats)
            })
            st.bar_chart(chart_data.set_index('Players') , color="#f4a261")



   
    
