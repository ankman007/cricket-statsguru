import streamlit as st
import pandas as pd
import numpy as np
from analytics.DataProcessingModule import clean_dataframe
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    batting_players_odi = pd.read_csv("resources/batting_players_odi.csv")
    batting_players_t20 = pd.read_csv("resources/batting_players_t20.csv")
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

def display_batting_chart(batting_players, batting_series):
    
    if st.session_state.Batting_stats and st.session_state.Player_chosen:
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
            title=f"{st.session_state.Batting_stats} Distribution Among Players in {batting_series} matches",  
            yaxis_title=f"{st.session_state.Batting_stats}",
            xaxis_title="Player's Name",
            plot_bgcolor='white',  
            font=dict(family="Arial", size=12, color="black"),
            showlegend=False,
        )
        
        st.plotly_chart(fig)

def display_scatter_chart(batting_players, title, xaxis, yaxis, size, color):

    fig = px.scatter(
        batting_players,
        x=xaxis,
        y=yaxis,
        color=color,
        size=size,
        hover_name="Player",
        title=title
    )
    
    fig.update_xaxes(title_text=st.session_state.xaxis)
    fig.update_yaxes(title_text=st.session_state.yaxis)
    fig.update_layout(coloraxis_colorbar=dict(title=st.session_state.color))
    fig.update_layout(legend=dict(title=st.session_state.size))
    fig.update_traces(hoverinfo="text+name", text="Player")
    fig.update_layout(title=f"For {title}: {st.session_state.xaxis} VS {st.session_state.yaxis} VS {st.session_state.color} VS {st.session_state.size}")

    st.plotly_chart(fig)


# Main code 
def display_batting_stats():
    batting_players_odi, batting_players_t20 = load_data()
    st.header("Batting Performance Overview")

    series_type = st.selectbox('Select Cricket Match Type', ('ODI', 'T20'), key="Batting_Series")
    stat_type = st.selectbox('Select Stats of Players', batting_players_odi.columns[2:], key="Batting_stats", index=4)

    available_players_odi = list(batting_players_odi['Player'])
    available_players_t20 = list(batting_players_t20['Player'])

    if "Player_chosen" not in st.session_state:
        st.session_state["Player_chosen"] = []

    available_players = list(set(available_players_odi + available_players_t20))
    default_players = ['Karan KC', 'RK Paudel', 'DS Airee', 'K Bhurtel', 'B Yadav', 'Kushal Malla', 'A Saud', 'Aarif Sheikh', 'S Lamichhane', 'P Khadka']
    selected_players = st.multiselect('Select Players', available_players, default=default_players)

    st.session_state.Player_chosen = selected_players

    if series_type == 'ODI':
        display_batting_chart(batting_players_odi, 'ODI')
    elif series_type == 'T20':
        display_batting_chart(batting_players_t20, 'T20')

    options = ['Span','Matches','Innings','Not Outs','Runs','Highest Score','Average Score','Strike Rate','Century', 'Half-Century','Zero Run Outs']

    st.header("Multi Variable Scatter Plots ")

    xaxis = st.selectbox('X-Axis Variable', options, key="xaxis", index=4)
    yaxis = st.selectbox('Y-Axis Variable', options, key="yaxis", index=2)
    size = st.selectbox('Size ', options, key="size", index=5)
    color = st.selectbox('Color', options, key="color", index=6)

    display_scatter_chart(batting_players_odi, "ODI Matches", st.session_state.xaxis, st.session_state.yaxis, st.session_state.size, st.session_state.color)
    display_scatter_chart(batting_players_t20, "T20 Matches", st.session_state.xaxis, st.session_state.yaxis, st.session_state.size, st.session_state.color)


if __name__ == "__main__":
    display_batting_stats()