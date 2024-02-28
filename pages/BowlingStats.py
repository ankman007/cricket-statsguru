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

st.title("Bowling Stats!")

#loading the data 
bowling_players_odi = pd.read_csv("data/bowling_players_odi.csv")
bowling_players_t20 = pd.read_csv("data/bowling_players_t20.csv")


#cleaning the null values 
clean_dataframe(bowling_players_odi)
clean_dataframe(bowling_players_t20)

#extracting players without repeating
def my_union(column_1 , column_2):
    column_1 = set(column_1)
    column_2 = set(column_2)
    return list(column_1.union(column_2))

#changing the columns of the dataframe 
columns = ['Player' , 'Span' , 'Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken' , 'Best Inning Bowling' , 
           'Bowling Average' , 'Economy' , 'Strike Rate' , 'Five Wickets' , 'Ten Wickets' , 'Catches Taken' , 'Stumping Made' ]
bowling_players_odi.columns = columns 
bowling_players_t20.columns = columns 


#creating selectbox and sessions
series_type = st.selectbox(
    'Select Cricket Match Type' , 
    ('ODI' , 'T20') , 
    key = "Bowling_series"
)

stat_type = st.selectbox(
    'Select Stat of Players' ,
    columns[2::], 
    key='bowling_stats'
)

players = st.multiselect(
    'Select Players' , 
    my_union(bowling_players_odi['Player'] , bowling_players_t20['Player']), 
    key="Player_chosen"
)

#for ODI series
if st.session_state.Bowling_series == 'ODI':
    if st.session_state.bowling_stats:
        if st.session_state.Player_chosen:
            #filtering players
            filtered_players = bowling_players_odi[bowling_players_odi['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Player': filtered_players['Player'] , 
                f'{st.session_state.bowling_stats}': changing_to_float(filtered_players , st.session_state.bowling_stats)
            })
           
            st.bar_chart(chart_data.set_index('Player') , color="#f4a261")
            st.dataframe(chart_data.set_index('Player') ,width=800)



#Doing the same for T20 too!
if st.session_state.Bowling_series == 'T20':
    if st.session_state.bowling_stats:
        if st.session_state.Player_chosen:
            filtered_players = bowling_players_t20[bowling_players_t20['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Player': filtered_players['Player'] , 
                f'{st.session_state.bowling_stats}': changing_to_float(filtered_players , st.session_state.bowling_stats)
            })
            st.bar_chart(chart_data.set_index('Player') , color="#f4a261"  )
            st.dataframe(chart_data.set_index('Player') , width=800)