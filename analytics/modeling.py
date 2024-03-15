import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def load_data():
    odi_data = pd.read_csv("resources/nepal_odi_stats.csv")
    t20_data = pd.read_csv("resources/nepal_t20_stats.csv")
    return odi_data, t20_data

def predict_win(data, user_chosen_opponent, label_encoder):
    data['Nepal_Win'] = data.apply(lambda x: 1 if x['Winner'] == 'Nepal' else 0, axis=1)
    data['Opponent_Encoded'] = label_encoder.transform(data['Team 2'])
    X = data[['Opponent_Encoded']]
    y = data['Nepal_Win']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy:", accuracy)
    
    try:
        opponent_encoded = label_encoder.transform([user_chosen_opponent])[0]
        opponent_encoded_reshaped = opponent_encoded.reshape(1, -1)  
        prediction = model.predict(opponent_encoded_reshaped)
        return prediction[0]
    except ValueError as e:
        print(f"Opponent '{user_chosen_opponent}' not found in dataset")
        return None

def display_result(df, opponent, match_type, label_encoder):
    prediction = predict_win(df, opponent, label_encoder)
    match_result = "win" if prediction == 1 else "lose"
    prediction_text = f"<h3>According to our prediction, Nepal will {match_result} the {match_type} match against {opponent}.</h3>"
    with st.container(border=True):
        st.markdown(prediction_text, unsafe_allow_html=True)


def modeling():
    st.markdown('<h1 style="text-align: center; color: #9F4B37;">Match Outcome Predictor</h1>', unsafe_allow_html=True)

    df_odi, df_t20 = load_data()
    odi_opponents = df_odi[df_odi['Team 1'] != 'Nepal']['Team 1'].unique() 
    t20_opponents = df_t20[df_t20['Team 1'] != 'Nepal']['Team 1'].unique()
    
    selected_match_type = st.selectbox('Select the match type: ', ['ODI', 'T20'], index=0, key='type_match')

    if selected_match_type == 'ODI':
        selected_opponent = st.selectbox(f'Select opponent for {selected_match_type} match prediction', odi_opponents, key='odi_options')
        label_encoder = LabelEncoder()
        label_encoder.fit(df_odi['Team 2'])  
        display_result(df_odi, selected_opponent, selected_match_type, label_encoder)

    if selected_match_type == 'T20':
        selected_opponent = st.selectbox(f'Select opponent for {selected_match_type} match prediction', t20_opponents, key='t20_options')
        label_encoder = LabelEncoder()
        label_encoder.fit(df_t20['Team 2'])  
        display_result(df_t20, selected_opponent, selected_match_type, label_encoder)
    st.markdown("""
        <p style="color:red; font-style: italic;">
            Note: This feature is still under development. Due to limited resources, predictions may not be entirely accurate. Please use this information judiciously.
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    modeling()