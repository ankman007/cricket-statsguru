import streamlit as st
from analytics import modeling

def set_page_configuration():
    st.set_page_config(
        page_title="Match Win Prediction",
        page_icon="🏆",
        layout="centered",
        initial_sidebar_state="expanded",
    )

def main():
    # set_page_configuration()
    # tab_titles = [
    #     'Winner Prediction',
    # ]
    # tabs = st.tabs(tab_titles)
    # with tabs[0]:
    modeling.modeling()

if __name__ == '__main__':
    main()
