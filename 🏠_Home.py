import streamlit as st

st.set_page_config(
    page_title="Cricket StatsGuru",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

def display_project_introduction():
    logo = "resources/images/cricket_statsguru.png"
    st.image(logo)  
    st.markdown('# Project Introduction')
    st.markdown('Cricket StatsGuru is a dynamic dashboard that contains visualization, analytics and modeling tools for Nepali cricket enthusiasts. This Streamlit-based web application provides a number of features specially tailored to enhance your understanding and enjoyment behind the runs and wickets. Whether you’re a lifelong cricket fan or a casual observer, we’ve got something for you. So, stick around and embark on an immersive Nepali cricket experience like never before!')

def featured_content():
    st.markdown("## Features 🌟")
    st.markdown("- Visualize the performance of your favorite Nepali cricketers side by side to compare their achievements.")
    st.markdown("- Explore in-depth batting and bowling statistics to uncover the secrets behind their success.")
    st.markdown("- Immerse yourself in the overall journey of the Nepali cricket team, from triumphs to challenges.")
    st.markdown("- Get historical insights into the evolution of Nepali cricket with an archive of past records and achievements.")
    st.markdown("- Engage with interactive charts and graphs, making statistical analysis both informative and enjoyable.")
    st.markdown("## Sections 📊")
    st.markdown("- **Player Profile**: Get insights into individual players' achievements, records, and milestones.")
    st.markdown("- **Team Statistics**: Dive into comprehensive statistics showcasing the team's performance over time.")
    st.markdown("- **Tournament Tracker**: Stay updated on upcoming fixtures, match results, and tournament standings.")
    st.markdown("- **Player Comparison**: Compare players head-to-head and discover the legends of Nepali cricket.")
    st.markdown("- **News and Updates**: Stay informed with the latest news, articles, and developments in Nepalese cricket.")
    st.markdown("- **Performance Analysis**: Analyze player and team performances through interactive heatmaps and trend visualizations.")

def display_sources():
    st.markdown('# Our Sources')

def main():
    tab1, tab2, tab3 = st.tabs(["Project Introduction", "Featured Content", "Our Sources"])

    with tab1:
        display_project_introduction()

    with tab2:
        featured_content()
    
    with tab3:
        display_sources()

if __name__ == "__main__":
    main()