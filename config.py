"""
NutriAI Configuration Module
Configuration schema and defaults for the application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'gym-nutrition-ai-secret-key-2024')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    TESTING = False
    
    # Server Configuration
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    # ML Model Configuration
    MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
    CALORIE_MODEL_PATH = os.path.join(MODEL_DIR, 'calorie_model.pkl')
    PROTEIN_MODEL_PATH = os.path.join(MODEL_DIR, 'protein_model.pkl')
    FEATURES_PATH = os.path.join(MODEL_DIR, 'model_features.pkl')
    ENCODERS_PATH = os.path.join(MODEL_DIR, 'label_encoders.pkl')
    
    # Feature Configuration
    FEATURES = [
        'Age', 'Gender', 'Weight', 'Height', 'BMI',
        'Workout_Frequency', 'Workout_Type', 'Experience_Level',
        'Session_Duration', 'Water_Intake', 'Fat_Percentage',
        'Physical_Exercise', 'Goal'
    ]
    
    # Input Validation Ranges
    VALIDATION_RANGES = {
        'age': {'min': 18, 'max': 100},
        'weight': {'min': 30, 'max': 200},
        'height': {'min': 120, 'max': 250},
        'workout_frequency': {'min': 1, 'max': 7},
        'session_duration': {'min': 30, 'max': 180},
        'water_intake': {'min': 1, 'max': 5},
        'fat_percentage': {'min': 5, 'max': 50},
        'physical_exercise': {'min': 0, 'max': 2},
    }
    
    # Categorical Options
    CATEGORICAL_OPTIONS = {
        'gender': ['Male', 'Female'],
        'workout_type': ['Cardio', 'Strength', 'Mixed', 'Flexibility'],
        'experience_level': ['Beginner', 'Intermediate', 'Advanced'],
        'physical_exercise': ['None', 'Light', 'Moderate'],
        'goal': ['Weight Loss', 'Maintenance', 'Muscle Gain'],
    }
    
    # BMR Calculation Parameters (Harris-Benedict)
    BMR_MALE_PARAMS = {
        'constant': 88.362,
        'weight_coeff': 13.397,
        'height_coeff': 4.799,
        'age_coeff': 5.677,
    }
    
    BMR_FEMALE_PARAMS = {
        'constant': 447.593,
        'weight_coeff': 9.247,
        'height_coeff': 3.098,
        'age_coeff': 4.330,
    }
    
    # Activity Factors for TDEE Calculation
    ACTIVITY_FACTORS = {
        1: 1.2,      # Sedentary
        2: 1.375,    # Light
        3: 1.55,     # Moderate
        4: 1.725,    # Heavy
        5: 1.9,      # Very Heavy
        6: 1.9,      # Athlete
        7: 1.9,      # Athlete
    }
    
    # Goal-Based Adjustments
    GOAL_ADJUSTMENTS = {
        'Weight Loss': {
            'calorie_multiplier': 0.85,
            'protein_multiplier': 1.05,
            'description': 'Create a 15% calorie deficit'
        },
        'Maintenance': {
            'calorie_multiplier': 1.0,
            'protein_multiplier': 1.0,
            'description': 'Maintain current weight'
        },
        'Muscle Gain': {
            'calorie_multiplier': 1.1,
            'protein_multiplier': 1.1,
            'description': 'Create a 10% calorie surplus'
        },
    }
    
    # Protein Requirements (g/kg body weight)
    PROTEIN_REQUIREMENTS = {
        'Weight Loss': 1.8,
        'Maintenance': 1.6,
        'Muscle Gain': 2.0,
    }
    
    # UI Configuration
    UI_CONFIG = {
        'theme': 'dark',
        'accent_color': '#7c3aed',
        'secondary_color': '#06b6d4',
        'animations_enabled': True,
        'glassmorphism_enabled': True,
    }
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_REFRESH_EACH_REQUEST = True
    
    # CORS Configuration (for future API)
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        pass


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Add production-specific settings here


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    # Override any specific settings for testing


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration for specified environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, DevelopmentConfig)


# Validation helper functions
def validate_input(field_name, value):
    """Validate input against configuration ranges"""
    
    ranges = Config.VALIDATION_RANGES
    
    if field_name in ranges:
        min_val = ranges[field_name]['min']
        max_val = ranges[field_name]['max']
        
        try:
            val = float(value)
            if val < min_val or val > max_val:
                return False, f"{field_name} must be between {min_val} and {max_val}"
        except (ValueError, TypeError):
            return False, f"Invalid {field_name}"
    
    return True, "Valid"


def validate_category(field_name, value):
    """Validate categorical input"""
    
    options = Config.CATEGORICAL_OPTIONS
    
    if field_name in options:
        if value not in options[field_name]:
            return False, f"Invalid {field_name}. Choose from: {options[field_name]}"
    
    return True, "Valid"


def calculate_bmr(age, gender, weight, height):
    """Calculate Basal Metabolic Rate"""
    
    if gender.lower() == 'male':
        params = Config.BMR_MALE_PARAMS
    else:
        params = Config.BMR_FEMALE_PARAMS
    
    bmr = (params['constant'] +
           params['weight_coeff'] * weight +
           params['height_coeff'] * height -
           params['age_coeff'] * age)
    
    return max(bmr, 0)  # Ensure non-negative


def calculate_tdee(bmr, workout_frequency):
    """Calculate Total Daily Energy Expenditure"""
    
    activity_factor = Config.ACTIVITY_FACTORS.get(
        workout_frequency, Config.ACTIVITY_FACTORS[3]
    )
    
    tdee = bmr * activity_factor
    return max(tdee, 0)  # Ensure non-negative


def apply_goal_adjustment(calories, goal):
    """Apply goal-based adjustment to calorie requirement"""
    
    adjustment = Config.GOAL_ADJUSTMENTS.get(goal, {})
    multiplier = adjustment.get('calorie_multiplier', 1.0)
    
    return calories * multiplier


def get_protein_requirement(weight, goal):
    """Get protein requirement based on weight and goal"""
    
    ratio = Config.PROTEIN_REQUIREMENTS.get(goal, 1.6)
    return weight * ratio


# Export configuration
__all__ = [
    'Config',
    'DevelopmentConfig',
    'ProductionConfig',
    'TestingConfig',
    'config',
    'get_config',
    'validate_input',
    'validate_category',
    'calculate_bmr',
    'calculate_tdee',
    'apply_goal_adjustment',
    'get_protein_requirement',
]
