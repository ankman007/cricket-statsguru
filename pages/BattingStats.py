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
batting_players_odi['HS'] = batting_players_odi['HS'].str.replace(r'\*' , '' , regex=True)
batting_players_t20['HS'] = batting_players_t20['HS'].str.replace(r'\*' , '' , regex=True)

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

#changing missing values into 0 
batting_players_t20.fillna(0 , inplace = True)
batting_players_odi.fillna(0 , inplace = True)
#defining selectbox and sessions
series_type = st.selectbox(
    'Select Cricket Match Type' , 
    ('ODI' , 'T20') , 
    key = "Batting_Series"
)
stat_type = st.selectbox(
    'Select Stats of Players' , 
    columns[2:] , 
    key = "Batting_stats" , 
    index = 4
)
players = st.multiselect(
    'Select Players' , 
    my_union(batting_players_odi['Player'] , batting_players_t20['Player']) , 
    key = "Player_chosen" , 
    default= ['Karan KC' , 'RK Paudel' , 'DS Airee' , 'K Bhurtel']
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
           
            fig1 = px.bar(chart_data.sort_values(by=f"{st.session_state.Batting_stats}" , ascending=False) , x ="Player" , y=f"{st.session_state.Batting_stats}")
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
            fig2 = px.bar(chart_data.sort_values(by=f"{st.session_state.Batting_stats}" , ascending = False) , x = "Player" , y=f"{st.session_state.Batting_stats}")
            st.plotly_chart(fig2)
            # st.dataframe(chart_data.set_index('Player') , width= 800)

st.header("Some Noticeable Stats🏏")
st.markdown("Work is still in progress!!⚒️")

xaxis = st.selectbox(
    'X' , 
    ['Matches' , 'Innings' , 'Not Outs' , 'Runs Scored' , 'Highest Score' , 'Batting Average' , 'Strike Rate' , 'Hundreds' , 'Fifties' , 'Ducks'] , 
    key = "xaxis"  , 
    index= 0
)
yaxis = st.selectbox(
    'Y' , 
    ['Matches' , 'Innings' , 'Not Outs' , 'Runs Scored' , 'Highest Score' , 'Batting Average' , 
     'Strike Rate' , 'Hundreds' , 'Fifties' , 'Ducks'] , 
           key = "yaxis" , 
           index = 3
)
size = st.selectbox(
    'Size' , 
    ['Matches' , 'Innings' , 'Not Outs' , 'Runs Scored' , 'Highest Score' , 'Batting Average' , 
     'Strike Rate' , 'Hundreds' , 'Fifties' , 'Ducks'] , 
           key = "size" , 
           index = 4
)
color = st.selectbox(
    'Color' , 
    ['Matches' , 'Innings' , 'Not Outs' , 'Runs Scored' , 'Highest Score' , 'Batting Average' , 
     'Strike Rate' , 'Hundreds' , 'Fifties' , 'Ducks'] ,
           key = "color" ,
           index = 5
)


fig3 = px.scatter(batting_players_odi , x= st.session_state.xaxis , y = st.session_state.yaxis ,
                 color = st.session_state.color  , size = st.session_state.size ,
           hover_name="Player" , title="ODI Matches")
st.plotly_chart(fig3)

fig4 = px.scatter(batting_players_t20 , x= st.session_state.xaxis , y = st.session_state.yaxis ,
                 color = st.session_state.color  , size = st.session_state.size ,
           hover_name="Player" , title="T20 Matches")
st.plotly_chart(fig4)



   
    
