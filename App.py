import streamlit as st
from recommendation import recommend
import random

st.title("Diet Recommendation")


age = st.number_input("Age", min_value=0, max_value=150, step=1)
gender = st.radio("Gender", ["Male", "Female"])
height = st.number_input("Height (in cm)", min_value=0, max_value=300, step=1)
weight = st.number_input("Weight (in kg)", min_value=0, max_value=500, step=1)


exercise_level = st.slider("Exercise Level", min_value=0, max_value=3, step=1,
                           format="%d", key="exercise")

exercise_levels = {0: "No Exercise",
                   1: "Little Exercise",
                   2: "Moderate Exercise",
                   3: "High Exercise"}

b_number = st.slider("Number of items you need in breakfast", min_value=0, max_value=10, step=1,
                           format="%d", key="b_val")
l_number = st.slider("Number of items you need in lunch", min_value=0, max_value=10, step=1,
                           format="%d", key="l_val")
d_number = st.slider("Number of items you need in dinner", min_value=0, max_value=10, step=1,
                           format="%d", key="d_val")

if st.button("Submit"):
    p = 0.3
    f = 0.3
    bmi = (weight / height**2) * 10000
    if bmi < 18.5:
        p = 0.4
        f = 0.2
        st.write("Suggestion: Gain Weight")
    elif 18.5<bmi<24.5:
        st.write("Suggestion: Maintain Weight")
    else:
        st.write("Suggestion: Lose Weight")

    bmr = (10 * weight + 6.25 * height - 5 * age + 5) if gender == "Male" else (10 * weight + 6.25 * height - 5 * age - 161)
    td_val = 0
    if exercise_level == 0:
        td_val = bmr * 1.2
    elif exercise_level == 1:
        td_val = bmr * 1.375
    elif exercise_level == 2:
        td_val = bmr * 1.55
    else:
        td_val = bmr * 1.725
    
    user_carbohydrates = (td_val * 0.4) / 4
    user_protein = (td_val * p) / 4
    user_fats = (td_val * f) / 4

    carbs, pros, fats = recommend(user_carbohydrates, user_protein, user_fats)

    res  = []
    res.extend(carbs)
    res.extend(pros)
    res.extend(fats)

    breakfast = random.sample(res, b_number)
    for i in breakfast:
        res.remove(i)
    lunch = random.sample(res, l_number)
    for i in lunch:
        res.remove(i)
    dinner = random.sample(res, d_number)
    for i in dinner:
        res.remove(i)

    st.write("Breakfast:")
    st.dataframe(breakfast)

    st.write("Lunch:")
    st.dataframe(lunch)

    st.write("Dinner:")
    st.dataframe(dinner)
    pass
