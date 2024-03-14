import streamlit as st

def add_explanation_expander(explanation='Chart explanation for this particular chart is being added soon. Stay tuned. 😉'):
    with st.expander("See explanation"):
        st.markdown(explanation)