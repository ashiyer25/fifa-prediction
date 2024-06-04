import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
from Orange.data import *

app_mode = st.sidebar.selectbox('Select Page',['Home','Predict'])

def predictions(age,height_cm,weight_kg,eur_value,eur_wage,overall,pac,sho,pas,dri,defence,phy,weak_foot):
    # Load the model
    with open("fifa_model_predict.pkcls", "rb") as f:
        model_loaded = pickle.load(f)
        
    # Define the domain with variable names
    domain = Domain([
        ContinuousVariable("age"),
        ContinuousVariable("height_cm"),
        ContinuousVariable("weight_kg"),
        ContinuousVariable("value_eur"),
        ContinuousVariable("wage_eur"),
        ContinuousVariable("overall"),
        ContinuousVariable("pace"),
        ContinuousVariable("shooting"),
        ContinuousVariable("passing"),
        ContinuousVariable("dribbling"),
        ContinuousVariable("defending"),
        ContinuousVariable("physic"),
        ContinuousVariable("weak_foot")
    ])
    
    # Create a data table with the provided values
    data = Table(domain, [[age, height_cm, weight_kg, value_eur, wage_eur, overall, pace, shooting, passing, dribbling, defending, physic, weak_foot]])
    
    # Make predictions
    if st.button("Predict"):
        output = model_loaded(data)
        preds = model_loaded.domain.class_var.str_val(output)
        preds = "Expected Rating of the Player: " + preds
        st.success(preds)
        df = pd.DataFrame(dict(r=[pace, shooting, dribbling, defending, physic],theta=['Pace','Shooting','Dribbling','Defence', 'Physicality']))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        st.plotly_chart(fig)

if app_mode == 'Home': 
    st.title('Player Potential Estimator')
    st.image('image.jpg')
    st.markdown('''The following are the steps to utilise this tool:--
    
    1. If accessing through PC/Laptop device - On your Left hand side of the page, 
    under "Select Page", choose "Predict" via the drop down list. 
    
    2. If accessing through a mobile device, head to the top right corner of the 
    screen, tap on the ">" button, from the pane that shows up, follow the 
    same step as the previous one.
    
    3. Use the sliders to input details for the player whose potential is 
    to be determined.
    
    4. Click on "Predict" button at the end of the page to receive results. ''')
     
    

elif app_mode == 'Predict':
    st.title('Potential Prediction') 
    st.subheader('Fill in player details ')

    age = st.slider("Select Age of the player:", 15, 50, 15)
    height_cm = st.slider("Select height of the player:", 150, 210, 150)
    weight_kg = st.slider("Select weight of the player:", 40, 100, 50)
    value_eur = st.slider("Select current valuation of the player:", 1000000, 140000000, 1000000)
    wage_eur = st.slider("Select current weekly wage of the player:", 1000, 100000000, 100)
    overall = st.slider ("Select overall player rating:", 40, 100, 40)
    pace = st.slider ("Select player's pace:", 40, 100, 40)
    shooting = st.slider ("Select player's shooting accuracy:", 40, 100, 40)
    passing = st.slider ("Select player's passing accuracy:", 40, 100, 40)
    dribbling = st.slider ("Select player's dribbling rating:", 40, 100, 40)
    defending = st.slider ("Select player's defensive capability rating:", 40, 100, 40)
    physic = st.slider ("Select player physicality rating:", 40, 100, 40)
    weak_foot = st.slider ("Select player's weak foot rating:", 1, 5, 1)
    
    predictions(age, height_cm, weight_kg, value_eur, wage_eur, overall, pace, shooting, passing, dribbling, defending, physic, weak_foot)