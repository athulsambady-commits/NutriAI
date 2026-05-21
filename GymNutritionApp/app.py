import os
import math
from flask import Flask, render_template, request, redirect, url_for, flash
import joblib
import numpy as np
import pandas as pd
from gemini_helper import generate_diet_plan

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'change-me')

# Attempt to load ML artifacts; fall back gracefully if missing
MODEL_PATH = os.path.join(os.path.dirname(__file__), '')

def safe_load(path):
    try:
        return joblib.load(path)
    except Exception:
        return None

calorie_model = safe_load(os.path.join(MODEL_PATH, 'calorie_model.pkl'))
protein_model = safe_load(os.path.join(MODEL_PATH, 'protein_model.pkl'))
model_features = safe_load(os.path.join(MODEL_PATH, 'model_features.pkl'))
label_encoders = safe_load(os.path.join(MODEL_PATH, 'label_encoders.pkl'))

ACTIVITY_FACTORS = {
    'Sedentary': 1.2,
    'Light': 1.375,
    'Moderate': 1.55,
    'Heavy': 1.725,
    'Athlete': 1.9
}

def calc_bmr(gender, weight, height, age):
    # weight in kg, height in cm, age in years
    if gender.lower() in ['male', 'm']:
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calc_tdee(bmr, activity_level):
    factor = ACTIVITY_FACTORS.get(activity_level, 1.375)
    return bmr * factor

def fallback_predictions(weight, tdee, goal):
    # Simple deterministic fallback when models aren't available
    if goal == 'Weight Loss':
        calories = max(1200, tdee - 500)
        protein = weight * 1.6
    elif goal == 'Muscle Gain':
        calories = tdee + 300
        protein = weight * 2.0
    else:
        calories = tdee
        protein = weight * 1.2
    return round(calories), round(protein)

def ml_predict(user_df, features):
    # If models are present, use them; otherwise use fallback logic
    try:
        if calorie_model is not None and protein_model is not None and features is not None:
            X = user_df[features]
            cal = calorie_model.predict(X)[0]
            prot = protein_model.predict(X)[0]
            return round(float(cal)), round(float(prot))
    except Exception:
        pass
    # fallback
    tdee = user_df.get('tdee', [0])[0] if isinstance(user_df, dict) else 0
    weight = user_df.get('Weight', [0])[0] if isinstance(user_df, dict) else 0
    goal = user_df.get('Goal', ['Maintenance'])[0] if isinstance(user_df, dict) else 'Maintenance'
    return fallback_predictions(weight, tdee, goal)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        # Parse numeric inputs safely
        age = int(data.get('age', 25))
        gender = data.get('gender', 'Male')
        weight = float(data.get('weight', 70))
        height = float(data.get('height', 170))
        bmi = data.get('bmi', '')
        if not bmi:
            bmi = round(weight / ((height/100)**2), 1)
        else:
            bmi = float(bmi)
        workout_freq = data.get('workout_freq', '3')
        workout_type = data.get('workout_type', 'Strength')
        experience = data.get('experience', 'Beginner')
        session_duration = float(data.get('session_duration', 60))
        water_intake = float(data.get('water_intake', 2.5))
        fat_percentage = float(data.get('fat_percentage', 20))
        physical_exercise = data.get('physical_exercise', 'Moderate')
        goal = data.get('goal', 'Maintenance')

        bmr = calc_bmr(gender, weight, height, age)
        tdee = calc_tdee(bmr, physical_exercise)

        # Prepare a simple dict for prediction or fallback
        user_dict = {
            'Age': [age],
            'Gender': [gender],
            'Weight': [weight],
            'Height': [height],
            'BMI': [bmi],
            'Workout Frequency': [workout_freq],
            'Workout Type': [workout_type],
            'Experience Level': [experience],
            'Session Duration': [session_duration],
            'Water Intake': [water_intake],
            'Fat Percentage': [fat_percentage],
            'Physical Exercise': [physical_exercise],
            'Goal': [goal],
            'tdee': [tdee]
        }

        calories, protein = ml_predict(user_dict, model_features if model_features else None)

        # Ensure reasonable defaults
        calories = int(calories or round(tdee))
        protein = int(protein or round(weight * 1.2))

        # Generate AI diet plan (Gemini or fallback)
        diet_plan = generate_diet_plan({
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'goal': goal,
            'calories': calories,
            'protein': protein
        })

        return render_template('result.html', calories=calories, protein=protein, bmi=bmi, goal=goal, diet_plan=diet_plan, water_intake=water_intake)
    except Exception as e:
        flash('An error occurred while processing your request.')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
