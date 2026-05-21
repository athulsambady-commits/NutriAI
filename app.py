"""
Gym Nutrition AI-Powered Recommendation Web Application
Flask backend with ML predictions and Gemini AI integration
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import os
from config import Config
from gemini_helper import GeminiDietPlanner, get_diet_planner
import traceback

app = Flask(__name__)
# Configuration
app.config['SECRET_KEY'] = 'gym-nutrition-ai-secret-key-2024'
app.config['JSON_SORT_KEYS'] = False

# Global variables for models
models = {}
label_encoders = {}
model_features = []

def load_models():
    """Load trained ML models and encoders"""
    global models, label_encoders, model_features
    
    try:
        # Load pickle files from project directory
        models['calorie'] = joblib.load(Config.CALORIE_MODEL_PATH)
        models['protein'] = joblib.load(Config.PROTEIN_MODEL_PATH)
        model_features = joblib.load(Config.FEATURES_PATH)
        label_encoders = joblib.load(Config.ENCODERS_PATH)
        
        print("[OK] Models loaded successfully!")
        return True
    except FileNotFoundError as e:
        print(f"[WARN] Model files not found: {e}")
        print("Please run: python train_models.py")
        return False

def calculate_bmr(age, gender, weight, height):
    """Calculate Basal Metabolic Rate using Harris-Benedict formula"""
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def calculate_tdee(bmr, workout_frequency):
    """Calculate Total Daily Energy Expenditure"""
    activity_factors = {
        1: 1.2,    # Sedentary
        2: 1.375,  # Light
        3: 1.55,   # Moderate
        4: 1.725,  # Heavy
        5: 1.9,    # Very Heavy
        6: 1.9,
        7: 1.9
    }
    factor = activity_factors.get(workout_frequency, 1.5)
    return bmr * factor

def calculate_bmi(weight, height):
    """Calculate Body Mass Index"""
    height_m = height / 100
    return weight / (height_m ** 2)

def prepare_prediction_data(form_data):
    """Prepare and encode data for model prediction"""
    try:
        # Encode categorical variables
        gender_encoded = label_encoders['Gender'].transform([form_data['gender']])[0]
        workout_type_encoded = label_encoders['Workout_Type'].transform([form_data['workout_type']])[0]
        exp_level_encoded = label_encoders['Experience_Level'].transform([form_data['experience_level']])[0]
        goal_encoded = label_encoders['Goal'].transform([form_data['goal']])[0]
        
        # Create feature array in the correct order
        features_order = ['Age', 'Gender', 'Weight', 'Height', 'BMI', 'Workout_Frequency', 
                         'Workout_Type', 'Experience_Level', 'Session_Duration', 'Water_Intake', 
                         'Fat_Percentage', 'Physical_Exercise', 'Goal']
        
        data = {
            'Age': int(form_data['age']),
            'Gender': gender_encoded,
            'Weight': float(form_data['weight']),
            'Height': float(form_data['height']),
            'BMI': float(form_data['bmi']),
            'Workout_Frequency': int(form_data['workout_frequency']),
            'Workout_Type': workout_type_encoded,
            'Experience_Level': exp_level_encoded,
            'Session_Duration': int(form_data['session_duration']),
            'Water_Intake': int(round(float(form_data['water_intake']))),
            'Fat_Percentage': float(form_data['fat_percentage']),
            'Physical_Exercise': int(form_data['physical_exercise']),
            'Goal': goal_encoded
        }
        
        # Create feature array in correct order
        X = np.array([[data[feature] for feature in features_order]])
        return X
    except Exception as e:
        print(f"Error preparing data: {e}")
        raise

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/results')
def results():
    """Results page route"""
    return render_template('result.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Prediction route - handles form submission and generates recommendations"""
    try:
        # Get form data
        data = request.json if request.is_json else request.form
        
        # Extract and validate inputs
        age = int(data.get('age', 0))
        gender = data.get('gender', 'Male')
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        workout_frequency = int(data.get('workout_frequency', 3))
        workout_type = data.get('workout_type', 'Mixed')
        experience_level = data.get('experience_level', 'Beginner')
        session_duration = int(data.get('session_duration', 60))
        water_intake = float(data.get('water_intake', 2.5))
        fat_percentage = float(data.get('fat_percentage', 25))
        physical_exercise = int(data.get('physical_exercise', 1))
        goal = data.get('goal', 'Maintenance')
        
        # Validation
        if age < 18 or age > 100:
            return jsonify({'error': 'Age must be between 18 and 100'}), 400
        if weight < 30 or weight > 200:
            return jsonify({'error': 'Weight must be between 30 and 200 kg'}), 400
        if height < 120 or height > 250:
            return jsonify({'error': 'Height must be between 120 and 250 cm'}), 400
        if water_intake < 1 or water_intake > 5:
            return jsonify({'error': 'Water intake must be between 1 and 5 liters'}), 400
        
        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        
        # Add to form data for prediction
        form_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'bmi': bmi,
            'workout_frequency': workout_frequency,
            'workout_type': workout_type,
            'experience_level': experience_level,
            'session_duration': session_duration,
            'water_intake': water_intake,
            'fat_percentage': fat_percentage,
            'physical_exercise': physical_exercise,
            'goal': goal
        }
        
        # Prepare data for prediction
        X = prepare_prediction_data(form_data)
        
        # Make predictions
        predicted_calories = max(0, models['calorie'].predict(X)[0])
        predicted_protein = max(0, models['protein'].predict(X)[0])
        
        # Adjust based on goal
        if goal == 'Weight Loss':
            predicted_calories *= 0.9
            predicted_protein *= 1.05
        elif goal == 'Muscle Gain':
            predicted_calories *= 1.1
            predicted_protein *= 1.1
        
        # Calculate BMR and TDEE for reference
        bmr = calculate_bmr(age, gender, weight, height)
        tdee = calculate_tdee(bmr, workout_frequency)
        
        # Generate AI diet plan using Google Gemini
        profile = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'bmi': bmi,
            'goal': goal,
            'workout_type': workout_type,
            'workout_frequency': workout_frequency,
            'experience_level': experience_level,
            'session_duration': session_duration,
            'water_intake': water_intake,
            'calories': predicted_calories,
            'protein': predicted_protein,
        }
        try:
            diet_result = get_diet_planner().generate_diet_plan(profile)
            diet_plan = diet_result['plan']
            diet_plan_source = diet_result['source']
        except Exception as e:
            print(f"Error generating AI diet plan: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            diet_plan = GeminiDietPlanner.get_default_diet_plan(profile)
            diet_plan_source = 'fallback'
        
        # Prepare response
        response = {
            'success': True,
            'calculations': {
                'bmi': round(bmi, 2),
                'bmr': round(bmr, 0),
                'tdee': round(tdee, 0),
                'calories': round(predicted_calories, 0),
                'protein': round(predicted_protein, 2),
                'goal': goal,
                'water_intake': round(water_intake * 1000)  # liters -> ml
            },
            'user_info': {
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': height,
                'experience_level': experience_level,
                'workout_frequency': workout_frequency,
                'session_duration': session_duration
            },
            'diet_plan': diet_plan,
            'diet_plan_source': diet_plan_source
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in prediction: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500


@app.route('/refine-diet-plan', methods=['POST'])
def refine_diet_plan():
    """Refine an existing diet plan using user food habits/preferences."""
    try:
        data = request.json if request.is_json else request.form
        food_habits = (data.get('food_habits') or '').strip()
        current_plan = (data.get('current_plan') or '').strip()
        profile = data.get('profile') or {}

        if not food_habits:
            return jsonify({'error': 'Please provide your food habits/preferences.'}), 400
        if not current_plan:
            return jsonify({'error': 'Current diet plan is required for refinement.'}), 400

        safe_profile = {
            'age': profile.get('age'),
            'gender': profile.get('gender'),
            'weight': profile.get('weight'),
            'height': profile.get('height'),
            'goal': profile.get('goal'),
            'calories': profile.get('calories'),
            'protein': profile.get('protein'),
            'workout_type': profile.get('workout_type', 'Mixed'),
            'workout_frequency': profile.get('workout_frequency', 3),
            'experience_level': profile.get('experience_level', 'Intermediate'),
            'session_duration': profile.get('session_duration', 60),
            'water_intake': profile.get('water_intake', 2.5),
            'bmi': profile.get('bmi'),
        }

        result = get_diet_planner().generate_diet_plan(
            profile=safe_profile,
            food_habits=food_habits,
            existing_plan=current_plan,
        )
        return jsonify({'success': True, 'diet_plan': result['plan'], 'diet_plan_source': result['source']})
    except Exception as e:
        print(f"Error refining AI diet plan: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        fallback_plan = GeminiDietPlanner.get_default_diet_plan(
            safe_profile if 'safe_profile' in locals() else {},
            food_habits=food_habits if 'food_habits' in locals() else None,
        )
        return jsonify({
            'success': True,
            'diet_plan': fallback_plan,
            'diet_plan_source': 'fallback',
            'warning': 'Gemini unavailable; returned offline refined plan.'
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    planner = get_diet_planner()
    return jsonify({
        'status': 'healthy',
        'models_loaded': bool(models),
        'gemini_configured': planner.enabled,
        'gemini_model': Config.GEMINI_MODEL if planner.enabled else None,
        'app': 'Gym Nutrition AI Recommender'
    })

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("GYM NUTRITION AI RECOMMENDATION APP")
    print("=" * 60)
    
    # Load models
    if load_models():
        print("\n[OK] Starting Flask application...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n[ERROR] Failed to load models. Please train models first:")
        print("   python train_models.py")
