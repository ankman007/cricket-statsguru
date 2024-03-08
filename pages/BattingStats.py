import streamlit as st
import pandas as pd #battingStats-design-&-code-structure-changes
import numpy as np
from DataProcessingModule import clean_dataframe
import plotly.express as px

batting_players_odi = pd.read_csv("data/batting_players_odi.csv")
batting_players_t20 = pd.read_csv("data/batting_players_t20.csv")

# Reads batting data for ODI and T20 matches from CSV files
def load_data():
    batting_players_odi = pd.read_csv("data/batting_players_odi.csv")
    batting_players_t20 = pd.read_csv("data/batting_players_t20.csv")
    clean_dataframe(batting_players_odi)
    clean_dataframe(batting_players_t20)
    
    batting_players_odi['Highest Score'] = batting_players_odi['Highest Score'].str.replace(r'\*', '', regex=True)
    batting_players_t20['Highest Score'] = batting_players_t20['Highest Score'].str.replace(r'\*', '', regex=True)

    str_column = ['Span','Matches','Innings','Not Outs','Runs','Highest Score','Average Score','Strike Rate','Century',
    'Half-Century','Zero Run Outs']

    batting_players_t20[str_column] = batting_players_t20[str_column].apply(pd.to_numeric, errors='coerce')
    batting_players_odi[str_column] = batting_players_odi[str_column].apply(pd.to_numeric, errors='coerce')

    batting_players_t20.fillna(0, inplace=True)
    batting_players_odi.fillna(0, inplace=True)

    return batting_players_odi, batting_players_t20

# Displays a bar chart using Plotly Express based on the selected player's batting statistics.
def display_batting_chart(batting_players, batting_series):
    if st.session_state.get('Batting_stats') is not None and st.session_state.get('Player_chosen'):
        filtered_players = batting_players[batting_players['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Player': filtered_players['Player'] , 
                f'{st.session_state.Batting_stats}': filtered_players[st.session_state.Batting_stats]
            })
           
            fig1 = px.bar(chart_data.set_index('Player'))
            st.plotly_chart(fig1)
            # st.dataframe(chart_data.set_index('Player') , width= 800)



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
            # st.bar_chart(chart_data.set_index('Player') , color="#f4a261")
            fig2 = px.bar(chart_data.set_index('Player'))
            st.plotly_chart(fig2)
            # st.dataframe(chart_data.set_index('Player') , width= 800)

st.header("Some Noticeable Stats🏏")

columns = ['Player', 'Span', 'Matches', 'Innings', 'Not Outs', 'Runs', 'Highest Score', 'Average Score', 'Strike Rate', 'Century' 'Half-Century', 'Zero Run Outs']

xaxis = st.selectbox('X', columns, key="xaxis", index=0)
yaxis = st.selectbox('Y', columns, key="yaxis", index=3)
size = st.selectbox('Size', columns, key="size", index=4)
color = st.selectbox('Color', columns, key="color", index=5)

display_scatter_chart(batting_players_odi, "ODI Matches")
display_scatter_chart(batting_players_t20, "T20 Matches")
