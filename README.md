# 🏋️ NutriAI - AI-Powered Gym Nutrition Calculator

A premium, production-ready AI-powered nutrition recommendation web application built with Flask, Machine Learning, and Google Gemini AI. Get personalized daily nutrition recommendations based on your fitness profile.

![AI Gym Nutrition](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

### 🧠 AI-Powered Engine
- **Machine Learning Predictions**: RandomForestRegressor models trained on fitness data
- **Daily Calorie Predictions**: Accurate calorie requirements based on your profile
- **Daily Protein Predictions**: Optimized protein intake for your fitness goal
- **Harris-Benedict Formulas**: Scientific calorie calculations

### 🤖 Google Gemini AI Integration
- **Personalized Diet Plans**: AI-generated meal plans tailored to your needs
- **Indian Cuisine Focus**: Practical meals with local food options
- **Meal Timings**: Optimized meal schedule including pre/post-workout nutrition
- **Macronutrient Breakdown**: Detailed macro recommendations

### 🎨 Premium UI/UX
- **Glassmorphism Design**: Modern frosted glass effects
- **Dark Futuristic Theme**: SaaS dashboard aesthetics
- **Smooth Animations**: Fluid transitions and micro-interactions
- **Lucide Icons**: Beautiful, consistent iconography
- **Fully Responsive**: Works perfectly on all devices
- **High Performance**: Optimized animations and lazy loading

### 📊 Comprehensive Calculations
- BMI (Body Mass Index)
- BMR (Basal Metabolic Rate)
- TDEE (Total Daily Energy Expenditure)
- Goal-based adjustments (Weight Loss, Maintenance, Muscle Gain)
- Macro ratios (Protein, Carbs, Fats)

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0**: Web framework
- **Python 3.9+**: Programming language
- **Scikit-learn**: Machine learning library
- **Joblib**: Model serialization

### ML/AI
- **RandomForestRegressor**: Prediction models
- **Google Gemini 1.5 Flash**: AI diet planning
- **Google Generative AI SDK**: Gemini integration

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling with variables & animations
- **JavaScript (Vanilla)**: Interactivity
- **Jinja2**: Template engine

### Development
- **Jupyter Notebook**: Model training
- **Python-dotenv**: Environment configuration
- **Pandas**: Data handling
- **NumPy**: Numerical computing

## 📋 Prerequisites

Before you begin, ensure you have the following:

1. **Python 3.9 or higher**
   ```bash
   python --version
   ```

2. **pip** (Python package manager)
   ```bash
   pip --version
   ```

3. **Google Gemini API Key**
   - Go to [Google AI Studio](https://ai.google.dev/)
   - Click "Get API Key"
   - Create or select a project
   - Copy your API key

4. **Git** (optional, for version control)
   ```bash
   git --version
   ```

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

```bash
cd CalTracker
```

### Step 2: Create a Python Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Open `.env` and add your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 5: Train Machine Learning Models

The models are generated from synthetic data to ensure reproducibility:

```bash
python train_models.py
```

This will create:
- `calorie_model.pkl` - Calorie prediction model
- `protein_model.pkl` - Protein prediction model
- `model_features.pkl` - Feature names
- `label_encoders.pkl` - Categorical encoders

**Note**: If you want to view the training process in detail, open the Jupyter notebook:
```bash
jupyter notebook notebooks/training.ipynb
```

### Step 6: Run the Flask Application

```bash
python app.py
```

The application will start at:
```
http://127.0.0.1:5000
```

Open this URL in your web browser.

## 📱 Usage Guide

### 1. **Access the Application**
   - Open `http://localhost:5000` in your browser

### 2. **Fill Your Profile**
   - Enter your age, gender, weight, height
   - Select workout frequency and type
   - Choose your experience level
   - Enter session duration and water intake
   - Specify your body fat percentage
   - Select your fitness goal

### 3. **Get Recommendations**
   - Click "Generate AI Diet Plan"
   - Wait for AI processing
   - View your personalized results

### 4. **Review Results**
   - Daily calorie recommendation
   - Daily protein requirement
   - BMI and category
   - Macronutrient breakdown
   - AI-generated meal plan with timings
   - Water intake schedule

### 5. **Recalculate or Modify**
   - Click "Recalculate" to try different parameters
   - Click "Back Home" to start over

## 📊 Model Features

The ML models use 13 input features:

1. **Age** (18-100 years)
2. **Gender** (Male/Female)
3. **Weight** (30-200 kg)
4. **Height** (120-250 cm)
5. **BMI** (Auto-calculated)
6. **Workout Frequency** (1-7 days/week)
7. **Workout Type** (Cardio, Strength, Mixed, Flexibility)
8. **Experience Level** (Beginner, Intermediate, Advanced)
9. **Session Duration** (30-180 minutes)
10. **Water Intake** (1-5 liters/day)
11. **Fat Percentage** (5-50%)
12. **Physical Exercise** (None, Light, Moderate)
13. **Goal** (Weight Loss, Maintenance, Muscle Gain)

## 🧮 Calculation Logic

### BMR (Basal Metabolic Rate)

**Male:**
```
BMR = 88.362 + (13.397 × Weight) + (4.799 × Height) - (5.677 × Age)
```

**Female:**
```
BMR = 447.593 + (9.247 × Weight) + (3.098 × Height) - (4.330 × Age)
```

### TDEE (Total Daily Energy Expenditure)

```
TDEE = BMR × Activity Factor
```

**Activity Factors:**
- Sedentary (1-2 days/week): 1.2
- Light (3-4 days/week): 1.375
- Moderate (4-5 days/week): 1.55
- Heavy (6 days/week): 1.725
- Athlete (7 days/week): 1.9

### Goal-Based Adjustments

- **Weight Loss**: TDEE × 0.85 (15% deficit)
- **Maintenance**: TDEE × 1.0
- **Muscle Gain**: TDEE × 1.1 (10% surplus)

### Protein Recommendations

- **Weight Loss**: 1.8g per kg of body weight
- **Maintenance**: 1.6g per kg of body weight
- **Muscle Gain**: 2.0g per kg of body weight

## 🎨 UI/UX Highlights

### Design Features
- **Glassmorphism**: Frosted glass effect with backdrop blur
- **Color Palette**: Deep blue background with purple and cyan accents
- **Typography**: Poppins (headings) + Inter (body)
- **Animations**: Smooth fade-ins, slide-ups, floating effects
- **Icons**: Lucide icon library for consistency
- **Responsive Grid**: Mobile-first, adaptive layouts

### Accessibility
- WCAG 2.1 compliant
- Keyboard navigation support
- High contrast ratios
- Semantic HTML structure
- Reduced motion support

## 📁 Project Structure

```
CalTracker/
├── app.py                          # Flask main application
├── gemini_helper.py                # Google Gemini integration
├── train_models.py                 # Model training script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
│
├── notebooks/
│   └── training.ipynb             # Jupyter notebook for model training
│
├── templates/
│   ├── layout.html                # Base template
│   ├── index.html                 # Landing page with form
│   └── result.html                # Results dashboard
│
├── static/
│   ├── css/
│   │   └── style.css              # Custom CSS with glassmorphism
│   ├── js/
│   │   └── script.js              # JavaScript animations & interactions
│   └── images/                    # Image assets (future)
│
└── README.md                       # This file
```

## 🔑 API Key Setup

### Getting Your Google Gemini API Key

1. **Visit Google AI Studio**
   - Go to [ai.google.dev](https://ai.google.dev/)

2. **Create API Key**
   - Click "Get API Key"
   - Select or create a Google Cloud Project
   - Click "Create API Key"

3. **Copy Your Key**
   - Copy the generated API key

4. **Add to .env**
   ```
   GEMINI_API_KEY=your_key_here
   ```

5. **Verify Setup**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('GEMINI_API_KEY')[:20] + '...')"
   ```

## 🚨 Troubleshooting

### Models Not Found
**Error**: `FileNotFoundError: calorie_model.pkl not found`

**Solution**: 
```bash
python train_models.py
```

### API Key Issues
**Error**: `GEMINI_API_KEY environment variable not set`

**Solution**:
1. Create `.env` file in project root
2. Add your API key: `GEMINI_API_KEY=your_key`
3. Restart the application

### Port Already in Use
**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Change port in app.py
# app.run(port=5001)  # Use different port
```

Or kill the process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Virtual Environment Issues
**Solution**:
```bash
# Deactivate current env
deactivate

# Remove old env (optional)
rm -rf venv

# Create fresh env
python -m venv venv

# Activate and reinstall
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## 📈 Performance Optimization

### Caching
- Models are loaded once on startup
- Label encoders cached in memory
- Feature names pre-loaded

### Frontend Optimization
- Lazy loading for images
- CSS minification ready
- JavaScript code-splitting capable
- Reduced motion support

### Backend Optimization
- Connection pooling
- Efficient numpy operations
- Vectorized calculations

## 🔐 Security

### Best Practices Implemented
- Environment variables for sensitive data
- Input validation on all fields
- Error handling without exposing internals
- CORS considerations for future APIs
- No hardcoded secrets

### Additional Security (Production)
- Use HTTPS/SSL certificates
- Implement rate limiting
- Add authentication if needed
- Use environment-specific configs
- Enable CSRF protection
- Set secure headers

## 📦 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Heroku Deployment
```bash
heroku login
heroku create your-app-name
git push heroku main
```

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication & profiles
- [ ] Workout logging and tracking
- [ ] Progress visualization
- [ ] Recipe database integration
- [ ] Nutrition tracking
- [ ] Social sharing features
- [ ] Mobile app
- [ ] Advanced analytics

## 📚 Resources

- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **Google Gemini API**: [ai.google.dev](https://ai.google.dev/)
- **Scikit-learn**: [scikit-learn.org](https://scikit-learn.org/)
- **Lucide Icons**: [lucide.dev](https://lucide.dev/)

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI diet planning
- Scikit-learn for machine learning
- Flask for web framework
- Lucide for icons
- All open-source contributors

## 📞 Support

For issues, questions, or suggestions:

1. Check the troubleshooting section above
2. Review Flask and Gemini API documentation
3. Create an issue in the repository
4. Contact: your-email@example.com

---

**Built with ❤️ using Flask, ML, and Google Gemini AI**

Made for fitness enthusiasts who want personalized, AI-powered nutrition guidance.

```
  ╔═══════════════════════════════════╗
  ║   NutriAI - Your Fitness Coach    ║
  ║   Powered by Google Gemini AI     ║
  ╚═══════════════════════════════════╝
```

## 🎓 Educational Value

This project demonstrates:

- ✅ Full-stack web development (Flask)
- ✅ Machine learning integration (Scikit-learn)
- ✅ AI API integration (Google Gemini)
- ✅ Modern UI/UX design (Glassmorphism)
- ✅ Responsive web design
- ✅ Professional code structure
- ✅ Production-ready practices
- ✅ User authentication patterns
- ✅ Data validation & security
- ✅ Performance optimization

Perfect for portfolio building and final-year projects!

---

**Version**: 1.0.0  
**Last Updated**: May 2024  
**Status**: ✅ Production Ready
