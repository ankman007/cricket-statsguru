import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
from DataProcessingModule import  clean_dataframe


st.title("Bowling Stats!")
st.markdown("Work is still in progress!!⚒️")

#loading the data 
bowling_players_odi = pd.read_csv("data/bowling_players_odi.csv")
bowling_players_t20 = pd.read_csv("data/bowling_players_t20.csv")


#cleaning the null values 
clean_dataframe(bowling_players_odi)
clean_dataframe(bowling_players_t20)

#changing the data type of few columns 
str_column = ['Inns', 'Balls', 'Mdns', 'Runs', 'Wkts', 'BBI',
       'Ave', 'Econ', 'SR', '5', '10', 'Ct', 'St']
bowling_players_odi[str_column] = bowling_players_odi[str_column].apply(pd.to_numeric, errors='coerce')
bowling_players_t20[str_column] = bowling_players_t20[str_column].apply(pd.to_numeric, errors='coerce')

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

#Turning NaN into 0 
bowling_players_odi.fillna(0 , inplace=True)
bowling_players_t20.fillna(0 , inplace = True)


#creating selectbox and sessions
series_type = st.selectbox(
    'Select Cricket Match Type' , 
    ('ODI' , 'T20') , 
    key = "Bowling_series"
)

stat_type = st.selectbox(
    'Select Stat of Players' ,
    columns[2::], 
    key='bowling_stats' , 
    index = 5
)

players = st.multiselect(
    'Select Players' , 
    my_union(bowling_players_odi['Player'] , bowling_players_t20['Player']), 
    key="Player_chosen" , 
    default= ['S Lamichhane' , 'DS Airee' , 'Karan KC' , 'K Bhurtel']
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
                f'{st.session_state.bowling_stats}': filtered_players[st.session_state.bowling_stats]
            })
            fig1 = px.bar(chart_data.sort_values(by=f"{st.session_state.bowling_stats}" , ascending=False) ,x = "Player", y = f"{st.session_state.bowling_stats}")
            st.plotly_chart(fig1)
            # st.bar_chart(chart_data.set_index('Player') , color="#f4a261")
            # st.dataframe(chart_data.set_index('Player') ,width=800)



#Doing the same for T20 too!
if st.session_state.Bowling_series == 'T20':
    if st.session_state.bowling_stats:
        if st.session_state.Player_chosen:
            filtered_players = bowling_players_t20[bowling_players_t20['Player'].isin(st.session_state.Player_chosen)]

            #creating dataframe to create chart 
            chart_data = pd.DataFrame({
                'Player': filtered_players['Player'] , 
                f'{st.session_state.bowling_stats}': filtered_players[st.session_state.bowling_stats]
            })
            fig2 = px.bar(chart_data.sort_values(by=f"{st.session_state.bowling_stats}" , ascending=False), x ="Player" , y = f"{st.session_state.bowling_stats}")
            st.plotly_chart(fig2)
            # st.dataframe(chart_data.set_index('Player') , width=800)
            
st.header("Some Noticeable Stats🏏")

xaxis = st.selectbox(
    'X' , 
    ['Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken' , 
           'Bowling Average' , 'Economy' , 'Strike Rate'] , 
    key = "xaxis"  , 
    index= 2
)
yaxis = st.selectbox(
    'Y' , 
    ['Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken',  
           'Bowling Average' , 'Economy' , 'Strike Rate'] , 
           key = "yaxis" , 
           index = 5
)
size = st.selectbox(
    'Size' , 
    ['Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken' ,
           'Bowling Average' , 'Economy' , 'Strike Rate'] , 
           key = "size" , 
           index = 7
)
color = st.selectbox(
    'Color' , 
    ['Matches' , 'Innings' , 'Balls' , 'Maidens' ,'Runs Conceded' , 'Wickets Taken' ,
           'Bowling Average' , 'Economy' , 'Strike Rate'] ,
           key = "color" ,
           index = 0
)


fig3 = px.scatter(bowling_players_odi , x= st.session_state.xaxis , y = st.session_state.yaxis ,
                 color = st.session_state.color  , size = st.session_state.size ,
           hover_name="Player" , title="ODI Stats")
st.plotly_chart(fig3)

fig4 = px.scatter(bowling_players_t20 , x= st.session_state.xaxis , y = st.session_state.yaxis ,
                 color = st.session_state.color  , size = st.session_state.size ,
           hover_name="Player" , title="T20 Stats")
st.plotly_chart(fig4)