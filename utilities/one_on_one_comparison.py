import streamlit as st
from utilities import batting_stats, bowling_stats
import pandas as pd
import plotly.express as px


# Loading data
def load_cricket_data():
    batting_players_odi, batting_players_t20 = batting_stats.load_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.load_bowling_data()
    bowling_players_odi, bowling_players_t20 = bowling_stats.set_column_names(bowling_players_odi, bowling_players_t20)
    bowling_players_odi, bowling_players_t20 = bowling_stats.fill_null_values(bowling_players_odi, bowling_players_t20)
    return batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20

def create_selectbox(series):
    #creating columns for the selectboxes 
    column_1  , column_3 = st.columns(2)
    with column_1: 
        player_1 = st.selectbox(
            "Select a player" , 
            series , 
            key="Player_1" , 
            index = list(series).index("RK Paudel")
            )
    with column_3:
        
        player_2 = st.selectbox(
            "Select a player" , 
            series , 
            key="Player_2" , 
            index = list(series).index("Karan KC"))
@st.cache_data
def loading_info_data():
    df = pd.read_csv("resources/players_info.csv")
    return df       
def showing_info():
    data = loading_info_data()
    column1 , column2 = st.columns(2)
    with column1: 
        try: 
            age = int(data[data['Name'] == st.session_state.Player_1]['Age'].iloc[0])
        except:
            age = "Unknown"
        st.markdown(f" **Full Name:** {data[data['Name'] == st.session_state.Player_1]['Full name'].iloc[0]}")
        st.image(data[data['Name'] == st.session_state.Player_1]['Photo'].iloc[0] , width=250)
        st.markdown(f" **Age:** {age}")
        st.markdown(f" **Batting Style:** {data[data['Name'] == st.session_state.Player_1]['Batting Style'].iloc[0]}")
        st.markdown(f" **Bowling Style:** {data[data['Name'] == st.session_state.Player_1]['Bowling Style'].iloc[0]}")
        st.markdown(f" **Playing Order:** {data[data['Name'] == st.session_state.Player_1]['Playing Order'].iloc[0]}")
    with column2:
        try: 
            age = int(data[data['Name'] == st.session_state.Player_2]['Age'].iloc[0])
        except:
            age = "Unknown"
        st.markdown(f" **Full Name:** {data[data['Name'] == st.session_state.Player_2]['Full name'].iloc[0]}")
        st.image(data[data['Name'] == st.session_state.Player_2]['Photo'].iloc[0] , width = 250)
        st.markdown(f" **Age:** {int(data[data['Name'] == st.session_state.Player_2]['Age'].iloc[0])}")
        st.markdown(f" **Batting Style:** {data[data['Name'] == st.session_state.Player_2]['Batting Style'].iloc[0]}")
        st.markdown(f" **Bowling Style:** {data[data['Name'] == st.session_state.Player_2]['Bowling Style'].iloc[0]}")
        st.markdown(f" **Playing Order:** {data[data['Name'] == st.session_state.Player_2]['Playing Order'].iloc[0]}")


#creating pie charts for respective stats
def create_pies(odi_df , t20_df  , player, column):
    try:
        odi_stat = odi_df[odi_df['Player'] == player][column].iloc[0]
    except:
        odi_stat = 0
    try:
        t20_stat = t20_df[t20_df["Player"]== player][column].iloc[0]
    except:
        t20_stat = 0
    # Create a DataFrame for the pie chart
    pie_data = pd.DataFrame({
        'Series Type': ['ODI', 'T20'],
        f'{column}': [odi_stat, t20_stat]
    })
    colors = px.colors.qualitative.Pastel1
    # Create a pie chart using Plotly Express
    fig = px.pie(pie_data, values=f'{column}' , color='Series Type', names='Series Type', title=f'Distribution of {player} {column} in ODI and T20' , color_discrete_sequence=colors , 
                hole = 0.6  , width=500)
    return fig





  
def showing_data(batting_players_odi , bowling_players_odi , batting_players_t20 , bowling_players_t20):
    column1 , column2 , column3 , column4 = st.columns(4)
    with column1:
        st.header("ODI Batting")
        selected_data = batting_players_odi[(batting_players_odi["Player"] == st.session_state.Player_1) | (batting_players_odi["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)

    with column2:
        st.header("ODI Bowling")
        selected_data = bowling_players_odi[(bowling_players_odi["Player"] == st.session_state.Player_1) | (bowling_players_odi["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)
    with column3:
        st.header("T20 Batting")
        selected_data = batting_players_t20[(batting_players_t20["Player"] == st.session_state.Player_1) | (batting_players_t20["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)
    with column4:
        st.header("T20 Bowling")
        selected_data = bowling_players_t20[(bowling_players_t20["Player"] == st.session_state.Player_1) | (bowling_players_t20["Player"] == st.session_state.Player_2)]
        st.dataframe(selected_data.set_index("Player").T)

#creating Pie charts for Specific columns 
def column_charts(odi_df , t20_df  , player1 , player2, column):
    column1 , column2 = st.columns(2)
    with column1:
        fig1 = create_pies(odi_df , t20_df  , player1, column)
        st.plotly_chart(fig1)
    with column2:
        fig2 = create_pies(odi_df , t20_df  , player2, column)
        st.plotly_chart(fig2)


def one_on_one_comparision():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 = load_cricket_data()
    player_info = loading_info_data()
    create_selectbox(player_info['Name'])
    showing_info()
    batting_columns = ['Matches','Innings','Not Outs','Runs','Highest Score','Average Score','Strike Rate','Century','Half-Century','Zero Run Outs']
    bowling_columns = ['Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken' , 'Bowling Average' , 'Economy' , 'Strike Rate' , 'Five Wickets' , 'Ten Wickets' , 'Catches Taken' , 'Stumping Made' ]
    # showing_data(batting_players_odi , bowling_players_odi , batting_players_t20 , bowling_players_t20)
    if st.session_state.rating_type == "Batting":
        stat1 = st.radio('Select Stat' , 
                        batting_columns ,
                        key = "stat1" , 
                        horizontal=True
                        )
        column_charts(batting_players_odi , batting_players_t20 , st.session_state.Player_1 , st.session_state.Player_2 , st.session_state.stat1)
    if st.session_state.rating_type == "Bowling":
        stat2 = st.radio('Select Stat' , 
                        bowling_columns ,
                        key = "stat2" , 
                        horizontal=True
                        )
        column_charts(bowling_players_odi , bowling_players_t20 , st.session_state.Player_1 , st.session_state.Player_2 , st.session_state.stat2)
    st.write("*Blank Chart Indicates there is no value")