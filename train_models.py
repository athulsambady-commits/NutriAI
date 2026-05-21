#!/usr/bin/env python3
"""
Model Training Script for Gym Nutrition Prediction
Generates trained RandomForestRegressor models for calorie and protein prediction
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

# Set random seed for reproducibility
np.random.seed(42)

# Define features
features = ['Age', 'Gender', 'Weight', 'Height', 'BMI', 'Workout_Frequency', 
            'Workout_Type', 'Experience_Level', 'Session_Duration', 'Water_Intake', 
            'Fat_Percentage', 'Physical_Exercise', 'Goal']

print("=" * 60)
print("GYM NUTRITION ML MODEL TRAINING")
print("=" * 60)
print(f"\nTotal features: {len(features)}")

# Generate synthetic training data
n_samples = 500

data = {
    'Age': np.random.randint(18, 65, n_samples),
    'Gender': np.random.choice(['Male', 'Female'], n_samples),
    'Weight': np.random.randint(45, 120, n_samples),  # kg
    'Height': np.random.randint(150, 200, n_samples),  # cm
    'Workout_Frequency': np.random.randint(1, 7, n_samples),  # days per week
    'Workout_Type': np.random.choice(['Cardio', 'Strength', 'Mixed', 'Flexibility'], n_samples),
    'Experience_Level': np.random.choice(['Beginner', 'Intermediate', 'Advanced'], n_samples),
    'Session_Duration': np.random.randint(30, 180, n_samples),  # minutes
    'Water_Intake': np.random.randint(1, 5, n_samples),  # liters per day
    'Fat_Percentage': np.random.uniform(10, 40, n_samples),
    'Physical_Exercise': np.random.randint(0, 3, n_samples),
    'Goal': np.random.choice(['Weight Loss', 'Maintenance', 'Muscle Gain'], n_samples)
}

# Calculate BMI
data['BMI'] = data['Weight'] / ((data['Height'] / 100) ** 2)

# Create DataFrame
df = pd.DataFrame(data)

# Generate realistic target values
def calculate_calories(row):
    """Calculate daily calorie requirement"""
    if row['Gender'] == 'Male':
        bmr = 88.362 + (13.397 * row['Weight']) + (4.799 * row['Height']) - (5.677 * row['Age'])
    else:
        bmr = 447.593 + (9.247 * row['Weight']) + (3.098 * row['Height']) - (4.330 * row['Age'])
    
    # Activity factor based on workout frequency
    activity_factors = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9, 6: 1.9, 7: 1.9}
    tdee = bmr * activity_factors.get(row['Workout_Frequency'], 1.5)
    
    # Goal adjustment
    if row['Goal'] == 'Weight Loss':
        tdee *= 0.85
    elif row['Goal'] == 'Muscle Gain':
        tdee *= 1.1
    
    return tdee + np.random.normal(0, 100)

def calculate_protein(row):
    """Calculate daily protein requirement"""
    if row['Goal'] == 'Muscle Gain':
        protein_ratio = 2.0  # 2g per kg
    elif row['Goal'] == 'Weight Loss':
        protein_ratio = 1.8  # 1.8g per kg
    else:
        protein_ratio = 1.6  # 1.6g per kg
    
    return row['Weight'] * protein_ratio + np.random.normal(0, 5)

df['Calories'] = df.apply(calculate_calories, axis=1)
df['Protein'] = df.apply(calculate_protein, axis=1)

print(f"\nDataset shape: {df.shape}")
print(f"Dataset statistics:")
print(df[['Calories', 'Protein', 'Weight', 'BMI']].describe())

# Encode categorical features
label_encoders = {}
categorical_features = ['Gender', 'Workout_Type', 'Experience_Level', 'Goal']

df_encoded = df.copy()

print("\nEncoding categorical features...")
for col in categorical_features:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"  {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# Prepare features and targets
X = df_encoded[features]
y_calories = df_encoded['Calories']
y_protein = df_encoded['Protein']

# Split data
X_train, X_test, y_cal_train, y_cal_test = train_test_split(X, y_calories, test_size=0.2, random_state=42)
_, _, y_prot_train, y_prot_test = train_test_split(X, y_protein, test_size=0.2, random_state=42)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train Calorie Model
print("\n" + "=" * 60)
print("Training Calorie Prediction Model...")
print("=" * 60)
calorie_model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
calorie_model.fit(X_train, y_cal_train)

cal_train_score = calorie_model.score(X_train, y_cal_train)
cal_test_score = calorie_model.score(X_test, y_cal_test)

print(f"Train Score: {cal_train_score:.4f}")
print(f"Test Score: {cal_test_score:.4f}")

# Train Protein Model
print("\n" + "=" * 60)
print("Training Protein Prediction Model...")
print("=" * 60)
protein_model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
protein_model.fit(X_train, y_prot_train)

prot_train_score = protein_model.score(X_train, y_prot_train)
prot_test_score = protein_model.score(X_test, y_prot_test)

print(f"Train Score: {prot_train_score:.4f}")
print(f"Test Score: {prot_test_score:.4f}")

# Save models
print("\n" + "=" * 60)
print("Saving Models...")
print("=" * 60)

model_dir = os.path.dirname(os.path.abspath(__file__))

joblib.dump(calorie_model, os.path.join(model_dir, 'calorie_model.pkl'))
joblib.dump(protein_model, os.path.join(model_dir, 'protein_model.pkl'))
joblib.dump(features, os.path.join(model_dir, 'model_features.pkl'))
joblib.dump(label_encoders, os.path.join(model_dir, 'label_encoders.pkl'))

print("[OK] Calorie Model saved: calorie_model.pkl")
print("[OK] Protein Model saved: protein_model.pkl")
print("[OK] Model Features saved: model_features.pkl")
print("[OK] Label Encoders saved: label_encoders.pkl")

print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETE!")
print("=" * 60)
