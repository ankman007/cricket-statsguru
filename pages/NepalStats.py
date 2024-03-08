import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data and preprocess
def load_data(url):
    df = pd.read_csv(url)
    
    # Attempt to convert 'Match Date' to datetime using multiple formats
    df['Match Date'] = pd.to_datetime(df['Match Date'], errors='coerce')
    
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
nepal_wins_by_year_odi = nepal_wins_odi.groupby('Year').size().reset_index(name='Wins')
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
    fig_odi = px.bar(nepal_odi_matches_results, x='Year', y=['Wins' , 'Losses'], title='Wins and Losses Of ODI matches over the years', text="Year")
    st.plotly_chart(fig_odi , use_container_width=True)

with tab2:
    fig_t20 = px.bar(nepal_t20_matches_results, x='Year', y=['Wins' , 'Losses'] , title='Wins and Losses Of T20 matches over the years' , text="Year")
    st.plotly_chart(fig_t20 , use_container_width=True)



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


st.header("Matches Played and wins by Ground🥇")

def create_colorful_bubble_chart(df, format_type):
    ground_counts = df['Ground'].value_counts().reset_index()
    ground_counts.columns = ['Ground', 'Number of Matches']

    fig = px.scatter(ground_counts, x='Ground', y='Number of Matches', size='Number of Matches', color='Number of Matches',
                     title=f'Number of {format_type} Matches Played in Each Ground',
                     labels={'Number of Matches': 'Number of Matches'},
                     size_max=40,  # Adjust the maximum bubble size as needed
                     color_continuous_scale='viridis')  # Choose a color scale

    fig.update_layout(xaxis_title='Ground', yaxis_title='Number of Matches Played')
    return fig 

#Function to create a bar chart for wins and losses on specific grounds
def create_bar_chart_all_teams(df, format_title):
    # Filter the data for wins and losses
    team_results = df[df['Winner'].notnull()]
    # Count the number of wins and losses for each ground
    ground_results_count = team_results.groupby(['Ground', 'Winner']).size().unstack(fill_value=0)
    # Calculate the total count for each ground and sort in descending order
    ground_results_count['Total'] = ground_results_count.sum(axis=1)
    ground_results_count = ground_results_count.sort_values(by='Total', ascending=False).drop(columns='Total')
    # Get unique winners (countries/teams) in the dataset
    unique_winners = df['Winner'].unique()
    # Set color sequence dynamically based on the number of unique winners
    color_sequence = px.colors.qualitative.Set1 if len(unique_winners) <= 10 else px.colors.qualitative.Plotly
    # Set labels dynamically based on unique winners
    labels = {winner: f'{winner} Wins' for winner in unique_winners}
    # Plot the bar chart
    fig = px.bar(ground_results_count, barmode='stack', color_discrete_sequence=color_sequence, labels=labels )
    fig.update_layout(title_text=f"All Teams Wins on Specific Grounds which against Nepal ({format_title})",
                      xaxis_title='Ground',
                      yaxis_title='Count',
                      xaxis=dict(tickangle=45, tickmode='array'),
                      bargap=0.2)
    return fig

def create_bar_chart(df, format_title , countries:list ):
    # Filter the data for Nepal wins and losses
    nepal_results = df[df['Winner'].isin(countries)]
    # Count the number of wins and losses for each ground
    ground_results_count = nepal_results.groupby(['Ground', 'Winner']).size().unstack(fill_value=0)
    # Calculate the total count for each ground and sort in descending order
    ground_results_count['Total'] = ground_results_count.sum(axis=1)
    ground_results_count = ground_results_count.sort_values(by='Total', ascending=False).drop(columns='Total')


    # Plot the bar chart
    fig = px.bar(ground_results_count, barmode='stack', color_discrete_sequence=px.colors.qualitative.Set1, 
                 labels={'Nepal':'Wins', 'U.A.E.':'Losses', 'Netherlands':'Losses'})
    fig.update_layout(title_text=f"Nepal {format_title} Wins and Losses on Specific Grounds",
                      xaxis_title='Ground',
                      yaxis_title='Count',
                      xaxis=dict(tickangle=45, tickmode='array'),
                      bargap=0.2)
    return fig 

match_type = st.selectbox(
    "Select match type" , 
    ["ODI" , "T20"] , 
    index = 0 , 
    key = "match_type"
)
graph_type = st.selectbox(
    "Select chart" , 
    ["Wins By Ground" , "Matches Played in grounds"] , 
    index = 0 , 
    key = "chart_type" 
)
opponent_options = st.multiselect(
            "Select Opponents *Only for Wins by ground!" , 
            my_union(t20_opponents , odi_opponents) , 
            key="bar_opponent" , 
)
countries = []
if st.session_state.match_type == "ODI":
    if st.session_state.chart_type == "Wins By Ground":
       
        countries = ["Nepal"] + st.session_state.bar_opponent
        fig_odi_ground = create_bar_chart(df_odi, 'ODI' , countries=countries)
        st.plotly_chart(fig_odi_ground , use_container_width=True)
    else: 
        st.plotly_chart(create_colorful_bubble_chart(df_odi, 'ODI') , use_container_width=True)

if st.session_state.match_type == "T20":
    if st.session_state.chart_type == "Wins By Ground":
        countries = ["Nepal"] + st.session_state.bar_opponent
        fig_t20_ground = create_bar_chart(df_t20, 'T20' , countries=countries)
        st.plotly_chart(fig_t20_ground , use_container_width=True)
    else:
        st.plotly_chart(create_colorful_bubble_chart(df_t20, 'T20') , use_container_width=True)



