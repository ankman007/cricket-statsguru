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

        chart_data = pd.DataFrame({
            'Player': filtered_players['Player'],
            f'{st.session_state.Batting_stats}': filtered_players[st.session_state.Batting_stats]
        })
        
        chart_data_sorted = chart_data.sort_values(by=f'{st.session_state.Batting_stats}', ascending=True)

        colors = ['#103f4e', '#0d5f6d']  

        fig = px.bar(chart_data_sorted, 
                     x='Player', 
                     y=f'{st.session_state.Batting_stats}',
                     color_discrete_sequence=colors)  
        
        fig.update_layout(
            # {Batting Stat} Distribution Among Players in {Match Type} Matches
            title=f"{st.session_state.Batting_stats} Distribution Among Players in {batting_series}",  # Title of the chart
            yaxis_title=f"{st.session_state.Batting_stats}",
            xaxis_title="Player's Name",
            plot_bgcolor='white',  
            font=dict(family="Arial", size=12, color="black"),
            showlegend=False,  
        )
        
        st.plotly_chart(fig)

# Displays a scatter plot using Plotly Express based on the selected player's batting statistics.
def display_scatter_chart(batting_players, title):
    fig = px.scatter(batting_players, x=st.session_state.xaxis, y=st.session_state.yaxis,
                     color=st.session_state.color, size=st.session_state.size,
                     hover_name="Player", title=title)
    st.plotly_chart(fig)

# Main code 
st.title("Batting Stats!")
batting_players_odi, batting_players_t20 = load_data()

if 'Batting_stats' not in st.session_state:
    st.session_state['Batting_stats'] = None

if 'Player_chosen' not in st.session_state:
    st.session_state['Player_chosen'] = []

series_type = st.selectbox('Select Cricket Match Type', ('ODI', 'T20'), key="Batting_Series")
stat_type = st.selectbox('Select Stats of Players', batting_players_odi.columns[2:], key="Batting_stats", index=4)

available_players_odi = list(batting_players_odi['Player'])
available_players_t20 = list(batting_players_t20['Player'])
available_players = list(set(available_players_odi + available_players_t20))

default_players = ['Karan KC', 'RK Paudel', 'DS Airee', 'K Bhurtel', 'B Yadav']
selected_players = st.multiselect('Select Players', available_players, default=default_players)
st.session_state['Player_chosen'] = selected_players

if series_type == 'ODI':
    display_batting_chart(batting_players_odi, 'ODI')
elif series_type == 'T20':
    display_batting_chart(batting_players_t20, 'T20')

st.header("Some Noticeable Stats🏏")

columns = ['Player', 'Span', 'Matches', 'Innings', 'Not Outs', 'Runs', 'Highest Score', 'Average Score', 'Strike Rate', 'Century' 'Half-Century', 'Zero Run Outs']

xaxis = st.selectbox('X', columns, key="xaxis", index=0)
yaxis = st.selectbox('Y', columns, key="yaxis", index=3)
size = st.selectbox('Size', columns, key="size", index=4)
color = st.selectbox('Color', columns, key="color", index=5)

display_scatter_chart(batting_players_odi, "ODI Matches")
display_scatter_chart(batting_players_t20, "T20 Matches")
