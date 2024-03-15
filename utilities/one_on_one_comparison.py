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
    column1 , column2  , column3= st.columns([4 , 2, 4])
    with column1: 
        try: 
            age = int(data[data['Name'] == st.session_state.Player_1]['Age'].iloc[0])
        except:
            age = "Unknown"
        st.image(data[data['Name'] == st.session_state.Player_1]['Photo'].iloc[0] , width=250)
        st.markdown(f"{data[data['Name'] == st.session_state.Player_1]['Full name'].iloc[0]}")
        st.markdown(f"{age}")
        st.markdown(f"{data[data['Name'] == st.session_state.Player_1]['Batting Style'].iloc[0]}")
        st.markdown(f"{data[data['Name'] == st.session_state.Player_1]['Bowling Style'].iloc[0]}")
        st.markdown(f"{data[data['Name'] == st.session_state.Player_1]['Playing Order'].iloc[0]}")
    
    with column2: 
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown("               ")
        st.markdown(" **Full Name** ")

        st.markdown(" **Age** ")
        st.markdown(" **Batting Style** ")
        st.markdown(" **Bowling Style** ")
        st.markdown(" **Playing Order** ")
    with column3:
        try: 
            age = int(data[data['Name'] == st.session_state.Player_2]['Age'].iloc[0])
        except:
            age = "Unknown"
        st.image(data[data['Name'] == st.session_state.Player_2]['Photo'].iloc[0] , width = 250)
        st.markdown(f"{data[data['Name'] == st.session_state.Player_2]['Full name'].iloc[0]}")
        st.markdown(f"{int(data[data['Name'] == st.session_state.Player_2]['Age'].iloc[0])}")
        st.markdown(f"{data[data['Name'] == st.session_state.Player_2]['Batting Style'].iloc[0]}")
        st.markdown(f"{data[data['Name'] == st.session_state.Player_2]['Bowling Style'].iloc[0]}")
        st.markdown(f"{data[data['Name'] == st.session_state.Player_2]['Playing Order'].iloc[0]}")


def chart(df1, df2, player1, player2, column):
    player_data = []
    for player in [player1, player2]:
        odi_stats = df1.loc[df1['Player'] == player, column].iloc[0] if player in df1['Player'].values else 0
        t20_stats = df2.loc[df2['Player'] == player, column].iloc[0] if player in df2['Player'].values else 0
        player_data.append([player, odi_stats, t20_stats])
        
    df = pd.DataFrame(player_data, columns=["Player", "ODI Matches", "T20 Matches"])
    
    fig = px.bar(df, x="Player", y=["ODI Matches", "T20 Matches"], barmode="group", 
                 color_discrete_sequence=px.colors.qualitative.Pastel1)
    
    # Customizing the layout
    fig.update_layout(
        title="Player Performance Comparison",
        xaxis_title="Player's Name",
        yaxis_title="Number of Matches",
        legend_title="Match Type",
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.2,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    # Customizing the bar colors
    fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.8)
    
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

def one_on_one_comparision():
    batting_players_odi, batting_players_t20, bowling_players_odi, bowling_players_t20 = load_cricket_data()
    player_info = loading_info_data()
    create_selectbox(player_info['Name'])
    showing_info()
    batting_columns = ['Matches','Innings','Not Outs','Runs','Highest Score','Average Score','Strike Rate','Century','Half-Century','Zero Run Outs']
    bowling_columns = ['Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken' , 'Bowling Average' , 'Economy' , 'Strike Rate' , 'Five Wickets' , 'Ten Wickets' , 'Catches Taken' , 'Stumping Made' ]
    # showing_data(batting_players_odi , bowling_players_odi , batting_players_t20 , bowling_players_t20)
    if st.session_state.rating_type == "Batting":
        stat1 = st.radio(' **Select Stat** ' , 
                        batting_columns ,
                        key = "stat1" , 
                        horizontal=True
                        )
        fig = chart(batting_players_odi , batting_players_t20 , st.session_state.Player_1 , st.session_state.Player_2 , st.session_state.stat1)
        st.plotly_chart(fig , use_container_width=True)
    if st.session_state.rating_type == "Bowling":
        stat2 = st.radio('Select Stat' , 
                        bowling_columns ,
                        key = "stat2" , 
                        horizontal=True
                        )
        fig = chart(bowling_players_odi , bowling_players_t20 , st.session_state.Player_1 , st.session_state.Player_2 , st.session_state.stat2)
        st.plotly_chart(fig , use_container_width=True)
    st.write("*Blank Chart Indicates there is no value")