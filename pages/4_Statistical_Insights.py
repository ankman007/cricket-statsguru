import streamlit as st
import pandas as pd
import plotly.express as px

def set_page_configuration():
    st.set_page_config(
        page_title="Statistical Insights",
        page_icon="⚾",
        layout="centered",
        initial_sidebar_state="expanded",
    )

def load_data(url):
    @st.cache_resource
    def _load_data(url):
        df = pd.read_csv(url)
        df['Match Date'] = pd.to_datetime(df['Match Date'], errors='coerce')
        df['Year'] = df['Match Date'].dt.year
        return df
    return _load_data(url)

def my_union(column_1, column_2):
    column_1 = set(column_1)
    column_2 = set(column_2)
    return list(column_1.union(column_2))

def filter_data(df):
    nepal_wins = df[df['Winner'] == 'Nepal']
    nepal_loss = df[df['Winner'] != 'Nepal']
    return nepal_wins, nepal_loss

def aggregate_results(nepal_wins, nepal_loss):
    wins_by_year = nepal_wins.groupby('Year').size().reset_index(name='Wins')
    loss_by_year = nepal_loss.groupby('Year').size().reset_index(name='Losses')
    merged_results = pd.merge(loss_by_year, wins_by_year, on='Year', how='inner')
    return merged_results


def display_bar_chart(odi_results, t20_results):
    selected_series = st.selectbox("Select Series", ["ODI", "T20"])
    if selected_series == "ODI":
        fig_matches_results = px.bar(odi_results, x='Year', y=['Wins', 'Losses'], 
                                      title='Nepal\'s ODI Match Win-Loss Analysis Over Time', barmode='group')
    else:
        fig_matches_results = px.bar(t20_results, x='Year', y=['Wins', 'Losses'], 
                                      title='Nepal\'s T20 Match Win-Loss Analysis Over Time', barmode='group')    
    fig_matches_results.update_layout(
        legend_title_text="Results",  
        legend=dict(
            orientation="h",  
            yanchor="bottom",  
            y=1.02,            
            xanchor="right",   
            x=1                
        )
    )
    
    fig_matches_results.update_layout(
        yaxis_title="Number of Wins/Losses",
        xaxis_title="Year",
        xaxis=dict(
            type='category'  
        )
    )

    st.plotly_chart(fig_matches_results, use_container_width=True)


def calculate_matchup_stats(df, team1, team2, matchup_type):
    matchups = df[((df['Team 1'] == team1) & (df['Team 2'] == team2)) | ((df['Team 1'] == team2) & (df['Team 2'] == team1))]
    matchups_stats = matchups.groupby('Winner').size().reset_index(name='Matches Won')
    return matchups_stats


def display_pie_chart(df_odi, df_t20, selected_opponent):    
    matchups_stats_odi = calculate_matchup_stats(df_odi, selected_opponent, 'Nepal', matchup_type='ODI')
    matchups_stats_t20 = calculate_matchup_stats(df_t20, selected_opponent, 'Nepal', matchup_type='T20')

    colors = px.colors.qualitative.Pastel1
    st.markdown(f"<p style='margin-top: 10px; font-weight: bold; font-size:25px'>Head-to-Head Comparison: Nepal vs. {selected_opponent}</p>", unsafe_allow_html=True)

    fig_odi = px.pie(matchups_stats_odi, names='Winner', values='Matches Won', 
                     title=f'ODI Match Win Distribution', hole=.5,
                     color_discrete_sequence=colors)
    
    fig_t20 = px.pie(matchups_stats_t20, names='Winner', values='Matches Won', 
                     title=f'T20 Match Win Distribution', hole=.5,
                     color_discrete_sequence=colors)

    fig_odi.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_t20.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    fig_odi.update_traces(pull=[0.1] * len(matchups_stats_odi['Winner']), textinfo='percent+label')
    fig_t20.update_traces(pull=[0.1] * len(matchups_stats_t20['Winner']), textinfo='percent+label')
    
    fig_odi.update_layout(font=dict(size=12))
    fig_t20.update_layout(font=dict(size=12))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_odi, use_container_width=True)
    with col2:
        st.plotly_chart(fig_t20, use_container_width=True)

    st.markdown("*Blank Chart indicates no Matches between teams")

def create_bar_chart(results_dataframe, match_type, countries: list):
    
    country_results = results_dataframe[results_dataframe['Winner'].isin(countries)]
    ground_results_count = country_results.groupby(['Ground', 'Winner']).size().unstack(fill_value=0)
    ground_results_count['Total'] = ground_results_count.sum(axis=1)
    ground_results_count = ground_results_count.sort_values(by='Total', ascending=False).drop(columns='Total')

    fig = px.bar(ground_results_count, barmode='stack', 
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 labels={country: 'Wins' if country in countries else 'Losses' for country in countries})

    fig.update_layout(
        title_text=f"Nepali Cricket Team's Win-Loss Record by Ground In {match_type} Matches",
        xaxis_title='Ground',
        yaxis_title='Number Of Wins/Losses',
        xaxis=dict(tickangle=45, tickmode='array'),
        bargap=0.2
    )

    return fig

def bubble_chart(df, format_type):
    ground_match_counts = df['Ground'].value_counts().reset_index()
    ground_match_counts.columns = ['Ground', 'Number of Matches']

    fig = px.scatter(ground_match_counts, x='Ground', y='Number of Matches', size='Number of Matches',
                     color='Number of Matches', title=f'Total {format_type} Matches Played Against Nepal by Venue',
                     labels={'Number of Matches': 'Number of Matches'},
                     size_max=40, color_continuous_scale='viridis')  

    fig.update_layout(xaxis_title='Match Locations', yaxis_title='Total Matches Played')

    return fig


def main():
    set_page_configuration()
    tab_titles = [
        'Series Overview',
        'Nepal Vs World',
        'Gorund Performance Analysis',
    ]
    tabs = st.tabs(tab_titles)

    
    odi_data_url = 'resources/nepal_odi_stats.csv'
    t20_data_url = 'resources/nepal_t20_stats.csv'
    df_odi = load_data(odi_data_url)
    df_t20 = load_data(t20_data_url)
    nepal_wins_odi, nepal_loss_odi = filter_data(df_odi)
    nepal_wins_t20, nepal_loss_t20 = filter_data(df_t20)
    nepal_odi_matches_results = aggregate_results(nepal_wins_odi, nepal_loss_odi)
    nepal_t20_matches_results = aggregate_results(nepal_wins_t20, nepal_loss_t20)

    with tabs[0]:
        display_bar_chart(nepal_odi_matches_results, nepal_t20_matches_results)

    
    
    
    with tabs[1]:
        odi_opponents = df_odi[df_odi['Team 1'] != 'Nepal']['Team 1'].unique() 
        t20_opponents = df_t20[df_t20['Team 1'] != 'Nepal']['Team 1'].unique()
        selected_opponent = st.selectbox('Select country', my_union(odi_opponents, t20_opponents), 
                                        key="opponent_selected", index=my_union(odi_opponents, t20_opponents).index("Netherlands"))
        matchup_type = st.selectbox("Select Matchup Type", ["ODI", "T20"])
        display_pie_chart(df_odi, df_t20, selected_opponent)
    
    with tabs[2]:
        match_type = st.selectbox("Select match type", ["ODI", "T20"], index=0, key="match_type")
        chart_type = st.selectbox("Select chart", ["Wins By Ground", "Matches Played in grounds"], index=0, key="chart_type")
        opponent_options = st.multiselect("Select Opponents *Only for Wins by ground!",
                                    my_union(t20_opponents, odi_opponents,),
                                    default=['Netherlands', 'U.S.A.', 'U.A.E.', 'Oman'],
                                    key="bar_opponent")

        if match_type == "ODI":
            if chart_type == "Wins By Ground":
                countries = ["Nepal"] + st.session_state.bar_opponent
                fig_odi_ground = create_bar_chart(df_odi, 'ODI', countries=countries)
                st.plotly_chart(fig_odi_ground, use_container_width=True)
            else: 
                st.plotly_chart(bubble_chart(df_odi, 'ODI'), use_container_width=True)
        if match_type == "T20":
            if chart_type == "Wins By Ground":
                countries = ["Nepal"] + st.session_state.bar_opponent
                fig_t20_ground = create_bar_chart(df_t20, 'T20', countries=countries)
                st.plotly_chart(fig_t20_ground, use_container_width=True)
            else:
                st.plotly_chart(bubble_chart(df_t20, 'T20'), use_container_width=True)

if __name__ == "__main__":
    main()
