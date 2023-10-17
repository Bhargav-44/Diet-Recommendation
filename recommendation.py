import pickle
import streamlit as st
import pandas as pd 

with open('diet.pkl', 'rb') as file:
    model_data = pickle.load(file)

knn_model = model_data['model']
scaler = model_data['scaler']
food = model_data['food_data']

def recommend(user_carbohydrates, user_protein, user_fat):    

    user_preferences_scaled = scaler.transform([[user_carbohydrates, user_protein, user_fat]])[0]

    distances, indices = knn_model.kneighbors([user_preferences_scaled[:1]]) 

    recommended_foods_carbohydrates = food.loc[indices[0]]['name'].tolist()

    food['protein'] = pd.to_numeric(food['protein'], errors='coerce')
    food['fats'] = pd.to_numeric(food['fats'], errors='coerce')

    remaining_protein = user_protein - food.loc[indices[0]]['protein'].sum()
    remaining_fat = user_fat - food.loc[indices[0]]['fats'].sum()

    knn_model.fit(food[['protein']])
    distances, indices = knn_model.kneighbors([[remaining_protein]])

    recommended_foods_protein = food.loc[indices[0]]['name'].tolist()

    knn_model.fit(food[['fats']])
    distances, indices = knn_model.kneighbors([[remaining_fat]])

    recommended_foods_fat = food.loc[indices[0]]['name'].tolist()

    return recommended_foods_carbohydrates,recommended_foods_protein,recommended_foods_fat
