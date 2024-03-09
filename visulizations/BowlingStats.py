import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
from DataProcessingModule import clean_dataframe

def load_bowling_data():
    bowling_players_odi = pd.read_csv("data/bowling_players_odi.csv")
    bowling_players_t20 = pd.read_csv("data/bowling_players_t20.csv")
    clean_dataframe(bowling_players_odi)
    clean_dataframe(bowling_players_t20)
    return bowling_players_odi, bowling_players_t20



def set_column_names(bowling_players_odi, bowling_players_t20):
    str_column = ['Span','Matches','Innings','Balls','Maidens','Runs','Wickets','Best Inning Bowling','Bowling Average','Economy Rate','Strike Rate','Five Wickets In An Innings','Ten Wickets In A Match','Caught','Stumped']
    bowling_players_odi[str_column] = bowling_players_odi[str_column].apply(pd.to_numeric, errors='coerce')
    bowling_players_t20[str_column] = bowling_players_t20[str_column].apply(pd.to_numeric, errors='coerce')
    columns = ['Player' , 'Span' , 'Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken' , 'Best Inning Bowling' , 'Bowling Average' , 'Economy' , 'Strike Rate' , 'Five Wickets' , 'Ten Wickets' , 'Catches Taken' , 'Stumping Made' ]
    bowling_players_odi.columns = columns 
    bowling_players_t20.columns = columns 
    return bowling_players_odi, bowling_players_t20



def fill_null_values(bowling_players_odi, bowling_players_t20):
    bowling_players_odi.fillna(0 , inplace=True)
    bowling_players_t20.fillna(0 , inplace = True)
    return bowling_players_odi, bowling_players_t20



def my_union(column_1 , column_2):
    column_1 = set(column_1)
    column_2 = set(column_2)
    return list(column_1.union(column_2))


def select_players(bowling_players_odi, bowling_players_t20):
    return st.multiselect(
        'Select Players', 
        my_union(bowling_players_odi['Player'], bowling_players_t20['Player']), 
        key="Player_chosen", 
        # default=['Sompal Kami', 'LN Rajbanshi', 'Karan KC', 'K Bhurtel', 'S Lamichhane', 'P Khadka', 'Aarif Sheikh', 'S Bhari', 'DS Airee']
    )

def display_bowling_chart(bowling_players, chart_title):
    if st.session_state.bowling_stats and st.session_state.Player_chosen:
        filtered_players = bowling_players[bowling_players['Player'].isin(st.session_state.Player_chosen)]
        chart_data = pd.DataFrame({
            'Player': filtered_players['Player'] , 
            f'{st.session_state.bowling_stats}': filtered_players[st.session_state.bowling_stats]
        })
        fig = px.bar(chart_data.sort_values(by=f"{st.session_state.bowling_stats}" , ascending=False) ,x = "Player", y = f"{st.session_state.bowling_stats}")

        chart_data_sorted = chart_data.sort_values(by=f'{st.session_state.bowling_stats}', ascending=True)

        colors = ['#103f4e', '#0d5f6d']  

        fig = px.bar(chart_data_sorted, 
                     x='Player', 
                     y=f'{st.session_state.bowling_stats}',
                     color_discrete_sequence=colors)  
        
        fig.update_layout(
            title=f"{st.session_state.bowling_stats} Distribution Among Players in {chart_title} matches",
            font=dict(family="Arial", size=12, color="black"),
            yaxis_title=f"{st.session_state.bowling_stats}",
            xaxis_title="Player's Name",
            plot_bgcolor='white',  
            showlegend=False,
        )
        
        st.plotly_chart(fig, use_container_width=True)
        # title=f"{st.session_state.Batting_stats} Distribution Among Players in {batting_series} matches",  

def display_scatter_chart(bowling_players, title, xaxis, yaxis, size, color):

    fig = px.scatter(
        bowling_players,
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

def display_bowling_stats():
    bowling_players_odi, bowling_players_t20 = load_bowling_data()
    bowling_players_odi, bowling_players_t20 = set_column_names(bowling_players_odi, bowling_players_t20)
    bowling_players_odi, bowling_players_t20 = fill_null_values(bowling_players_odi, bowling_players_t20)
    
    st.header("Bowling Performance Overview")

    
    series_type = st.selectbox('Select Cricket Match Type', ('ODI', 'T20'), key="Bowling_series")
    stat_type = st.selectbox('Select Stat of Players', bowling_players_odi.columns[2:], key='bowling_stats', index=5)
    players = select_players(bowling_players_odi, bowling_players_t20)
    
    if st.session_state.Bowling_series == 'ODI':
        display_bowling_chart(bowling_players_odi, 'ODI')
    elif st.session_state.Bowling_series == 'T20':
        display_bowling_chart(bowling_players_t20, 'T20')

    st.header("Multi Variable Scatter Plots ")
    options = ['Matches', 'Innings', 'Balls', 'Maidens', 'Runs Conceded', 'Wickets Taken', 'Bowling Average', 'Economy', 'Strike Rate']

    xaxis = st.selectbox('X Variable', options=options, key="x-axis", index=2)
    yaxis = st.selectbox('Y Variable', options=options, key="y-axis", index=5)
    size = st.selectbox('Size', options=options, key="size-1", index=7)
    color = st.selectbox('Color', options=options, key="color-1", index=0)

    display_scatter_chart(bowling_players_odi, "ODI Matches", xaxis, yaxis, size, color)
    display_scatter_chart(bowling_players_t20, "T20 Matches", xaxis, yaxis, size, color)


if __name__ == "__main__":
    display_bowling_stats()
