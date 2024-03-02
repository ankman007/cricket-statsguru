import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data and preprocess
def load_data(url):
    df = pd.read_csv(url, error_bad_lines=False)
    
    # Attempt to convert 'Match Date' to datetime using multiple formats
    df['Match Date'] = pd.to_datetime(df['Match Date'], errors='coerce', infer_datetime_format=True)
    
    # Extract year from the datetime column
    df['Year'] = df['Match Date'].dt.year
    
    return df

# Load ODI and T20 data
odi_data_url = 'data/nepal_odi_stats.csv'
t20_data_url = 'data/nepal_t20_stats.csv'

df_odi = load_data(odi_data_url)
df_t20 = load_data(t20_data_url)

# Filter data to include only matches where Nepal is the winner
nepal_wins_odi = df_odi[df_odi['Winner'] == 'Nepal']
nepal_wins_t20 = df_t20[df_t20['Winner'] == 'Nepal']

# Including Loses too!
nepal_loss_odi = df_odi[df_odi['Winner'] != 'Nepal']
nepal_loss_t20 = df_t20[df_t20['Winner'] != 'Nepal']

# Filter to include only years where there is valid data
nepal_wins_by_year_odi = nepal_wins_odi[nepal_wins_odi.Year >= 2018].groupby('Year').size().reset_index(name='Wins')
nepal_wins_by_year_t20 = nepal_wins_t20.groupby('Year').size().reset_index(name='Wins')

#Nepals Loses 
nepal_loss_by_year_odi = nepal_loss_odi.groupby('Year').size().reset_index(name='Losses')
nepal_loss_by_year_t20 = nepal_loss_t20.groupby('Year').size().reset_index(name = 'Losses')

#mergin wins and losses 
nepal_odi_matches_results = pd.merge(nepal_loss_by_year_odi , nepal_wins_by_year_odi ,on='Year' , how='inner')
nepal_t20_matches_results = pd.merge(nepal_loss_by_year_t20 , nepal_wins_by_year_t20 , on='Year' , how = 'inner')

st.markdown("""
    # This page is being build!⚒️
""")
st.markdown("""
    ### Matches Results by Nepal In ODI and T20 series till date.
""")
tab1 , tab2 = st.tabs(['ODI Wins' , 'T20 Wins'])

with tab1:
    fig_odi = px.bar(nepal_odi_matches_results, x='Year', y=['Wins' , 'Losses'], title='Wins and Losses Of ODI matches over the years')
    st.plotly_chart(fig_odi , use_container_width=True)
    st.table(nepal_odi_matches_results.set_index('Year'))
with tab2:
    fig_t20 = px.bar(nepal_t20_matches_results, x='Year', y=['Wins' , 'Losses'] , title='T20 Wins Over the Years')
    st.plotly_chart(fig_t20 , use_container_width=True)
    st.table(nepal_t20_matches_results.set_index('Year'))


st.markdown("### Matches result of Nepal against other countries.🆚")

def calculate_matchup_stats(df, team1, team2):
    matchups = df[((df['Team 1'] == team1) & (df['Team 2'] == team2)) | ((df['Team 1'] == team2) & (df['Team 2'] == team1))]
    matchups_stats = matchups.groupby('Winner').size().reset_index(name='Matches Won')
    return matchups_stats

#creating list of opponents 
odi_opponents = df_odi[df_odi['Team 1'] != 'Nepal']['Team 1'].unique() 
t20_opponents = df_t20[df_t20['Team 1'] != 'Nepal']['Team 1'].unique()

#extracting players without repeating
def my_union(column_1 , column_2):
    column_1 = set(column_1)
    column_2 = set(column_2)
    return list(column_1.union(column_2))

opponent_country = st.selectbox(
    'Select country' , 
    my_union(odi_opponents , t20_opponents) , 
    key= "opponent_selected"
)
col1 ,col2 = st.columns(2)
with col1:
    st.header("ODI matches")
    matchups_stats_odi = calculate_matchup_stats(df_odi, st.session_state.opponent_selected, 'Nepal')
    fig_odi_vs = px.pie(matchups_stats_odi, names='Winner', values='Matches Won', title=f'{st.session_state.opponent_selected} vs Nepal ODI Matchups')
    st.plotly_chart(fig_odi_vs , use_container_width=True )
    

with col2:
    st.header("T20 matches")
    matchups_stats_t20 = calculate_matchup_stats(df_t20, st.session_state.opponent_selected, 'Nepal')
    fig_t20_vs = px.pie(matchups_stats_t20, names='Winner', values='Matches Won', title=f'{st.session_state.opponent_selected} vs Nepal T20 Matchups')
    st.plotly_chart(fig_t20_vs , use_container_width=True )
st.markdown("*Blank Chart indicates no Matches between teams")