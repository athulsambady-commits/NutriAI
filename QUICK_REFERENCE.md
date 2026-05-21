# 📋 NutriAI - Quick Reference & Cheat Sheet

## 🚀 Quick Commands

### Setup & Installation
```bash
# Windows
setup.bat

# macOS/Linux
chmod +x setup.sh
./setup.sh

# Manual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Training Models
```bash
python train_models.py
```

### Running the App
```bash
python app.py
```

### Accessing the App
```
http://localhost:5000
```

### Deactivating Virtual Environment
```bash
deactivate
```

---

## 🔧 Environment Configuration

### .env File Template
```
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Getting Gemini API Key
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Copy the key
4. Add to .env: `GEMINI_API_KEY=your_key`

---

## 📊 Project Statistics

| Category | Details |
|----------|---------|
| **Backend** | Flask 3.0.0 |
| **Frontend** | HTML5, CSS3, Vanilla JS |
| **ML Framework** | Scikit-learn |
| **AI Integration** | Google Gemini API |
| **Python Version** | 3.9+ |
| **Database** | In-memory (models cached) |
| **Port** | 5000 |
| **CSS Lines** | 1000+ |
| **JS Lines** | 400+ |
| **Python Lines** | 1500+ |
| **HTML Lines** | 800+ |
| **Total Lines** | 3700+ |

---

## 🗂️ File Organization

```
CalTracker/
├── app.py (Flask Backend - 450 lines)
│   ├── Flask app initialization
│   ├── Model loading
│   ├── BMR/TDEE calculations
│   ├── Prediction routes
│   └── Gemini integration
│
├── gemini_helper.py (AI Integration - 150 lines)
│   ├── GeminiDietPlanner class
│   ├── Diet plan generation
│   └── Fallback diet plan
│
├── train_models.py (ML Training - 200 lines)
│   ├── Synthetic data generation
│   ├── Model training
│   ├── Feature engineering
│   └── Model serialization
│
├── templates/ (HTML - 800 lines)
│   ├── layout.html (Base template)
│   ├── index.html (Landing page)
│   └── result.html (Results dashboard)
│
├── static/ (Assets - 1400 lines)
│   ├── css/style.css (1000+ lines)
│   │   ├── Variables & colors
│   │   ├── Glassmorphism styles
│   │   ├── Animations
│   │   ├── Responsive layout
│   │   └── Dark theme
│   │
│   └── js/script.js (400+ lines)
│       ├── Form validation
│       ├── Scroll animations
│       ├── Loading states
│       ├── Number animations
│       └── Accessibility
│
└── notebooks/
    └── training.ipynb (Jupyter notebook)
```

---

## 🎨 Design System

### Color Palette
```css
--bg: #0f172a              /* Deep blue background */
--primary: #7c3aed         /* Purple */
--secondary: #06b6d4       /* Cyan */
--accent: #f43f5e          /* Rose */
--text: #f8fafc            /* Light text */
--text-secondary: #cbd5e1  /* Muted text */
--glass: rgba(255,255,255,0.08)  /* Glassmorphism */
```

### Typography
- **Headings**: Poppins (600-800 weight)
- **Body**: Inter (300-600 weight)
- **Size Scale**: 0.85rem to 3.5rem

### Spacing Scale
- xs: 0.25rem
- sm: 0.5rem
- md: 1rem
- lg: 2rem
- xl: 3rem
- 2xl: 4rem

### Border Radius
- sm: 0.375rem
- md: 0.75rem
- lg: 1.5rem
- xl: 2rem

---

## 🔌 API Endpoints

### Home
```
GET /
Returns: index.html (landing page)
```

### Results Page
```
GET /results
Returns: result.html (results dashboard)
Note: Requires data in sessionStorage
```

### Predictions
```
POST /predict
Headers: Content-Type: application/json

Request Body:
{
  "age": 25,
  "gender": "Male",
  "weight": 75,
  "height": 175,
  "workout_frequency": 4,
  "workout_type": "Mixed",
  "experience_level": "Intermediate",
  "session_duration": 60,
  "water_intake": 2.5,
  "fat_percentage": 20,
  "physical_exercise": 1,
  "goal": "Muscle Gain"
}

Response:
{
  "success": true,
  "calculations": {
    "bmi": 24.5,
    "bmr": 1700,
    "tdee": 2550,
    "calories": 2805,
    "protein": 150,
    "goal": "Muscle Gain",
    "water_intake": 625
  },
  "user_info": {...},
  "diet_plan": "AI generated diet plan text"
}
```

### Health Check
```
GET /health
Returns: {"status": "healthy", "models_loaded": true}
```

---

## 🧠 ML Model Details

### Features (13 Total)
1. Age (18-100 years)
2. Gender (M/F - encoded)
3. Weight (30-200 kg)
4. Height (120-250 cm)
5. BMI (auto-calculated)
6. Workout Frequency (1-7)
7. Workout Type (encoded)
8. Experience Level (encoded)
9. Session Duration (30-180 min)
10. Water Intake (1-5 L)
11. Fat Percentage (5-50%)
12. Physical Exercise (0-2)
13. Goal (encoded)

### Models
- **Calorie Model**: RandomForest (100 estimators, depth=20)
- **Protein Model**: RandomForest (100 estimators, depth=20)
- **Training Data**: 500 synthetic samples
- **Test Split**: 20%
- **Accuracy**: ~95%+ R² score

### Formulas
```
BMR (Male) = 88.362 + (13.397 × W) + (4.799 × H) - (5.677 × A)
BMR (Female) = 447.593 + (9.247 × W) + (3.098 × H) - (4.330 × A)
TDEE = BMR × Activity Factor
```

---

## 🎯 Form Inputs & Validation

| Field | Type | Range | Default | Validation |
|-------|------|-------|---------|-----------|
| Age | number | 18-100 | 25 | Required |
| Gender | select | M/F | Male | Required |
| Weight | number | 30-200 | 75 | Required |
| Height | number | 120-250 | 175 | Required |
| Workout Freq | number | 1-7 | 4 | Required |
| Workout Type | select | 4 options | Mixed | Required |
| Experience | select | 3 levels | Intermediate | Required |
| Duration | number | 30-180 | 60 | Required |
| Water Intake | number | 1-5 | 2.5 | Required |
| Fat % | number | 5-50 | 20 | Required |
| Exercise | select | 3 levels | Light | Required |
| Goal | select | 3 goals | Maintenance | Required |

---

## 🎬 Animations & Effects

### CSS Animations
- `slideInLeft`: Hero text entrance
- `slideInRight`: Hero visual entrance
- `slideUp`: Card reveals
- `float`: Blob movement
- `spin`: Loading spinner
- `slideIn`: Progress bars

### JavaScript Effects
- Scroll reveal on intersection
- Number counting animations
- Smooth scrolling
- Focus glow effects
- Hover transformations
- Particle animations

### Transitions
- Default: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- Fast: 0.15s ease-in-out
- Smooth: Natural easing

---

## 📱 Responsive Breakpoints

```css
/* Desktop */
Max: 1200px content width
Grid: Auto-fit columns

/* Tablet */
768px: Single column forms
768px: Stack features vertically

/* Mobile */
480px: Compact spacing
480px: Font size adjustments
480px: Full-width buttons
```

---

## 🔐 Security Features

- ✅ Input validation on all fields
- ✅ Environment variables for secrets
- ✅ No hardcoded API keys
- ✅ Error handling without exposure
- ✅ Range validation on all numeric inputs
- ✅ Type checking on form submission

### To Add (Production)
- [ ] HTTPS/SSL certificates
- [ ] Rate limiting
- [ ] CSRF protection
- [ ] Input sanitization
- [ ] Authentication
- [ ] Database encryption

---

## 📈 Performance Optimization Tips

### Frontend
```javascript
// Lazy loading images
// Debounced scroll handlers
// CSS animations (GPU accelerated)
// Minimized reflows/repaints
```

### Backend
```python
# Models loaded once on startup
# Vectorized numpy operations
# Efficient algorithm selection
# Connection pooling ready
```

### Deployment
```bash
# Use gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Enable compression
# Use CDN for static files
# Enable browser caching
# Minify CSS/JS
```

---

## 🐛 Debugging Checklist

- [ ] Models exist (.pkl files)
- [ ] .env file configured
- [ ] API key valid
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Port 5000 available
- [ ] Browser console clean (F12)
- [ ] Network requests successful
- [ ] Form values within range
- [ ] Gemini API responding

---

## 📚 Learning Paths

### Backend Development
1. Flask routing and views
2. Request/response handling
3. Template rendering
4. Error handling

### ML Integration
1. Model training (train_models.py)
2. Serialization with joblib
3. Data preprocessing
4. Feature scaling

### AI Integration
1. Gemini API authentication
2. Prompt engineering
3. Response parsing
4. Error handling

### Frontend
1. HTML structure
2. CSS styling (glassmorphism)
3. JavaScript interactions
4. Animations and effects

---

## 🚀 Deployment Platforms

### Free Options
- **Heroku** (student credits)
- **Render** (free tier)
- **Replit** (collaborative)
- **PythonAnywhere** (free option)

### Premium Options
- **AWS** (scalable)
- **Google Cloud** (enterprise)
- **Azure** (Microsoft ecosystem)
- **DigitalOcean** (affordable)

---

## 📞 Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| Python not found | Install Python 3.9+ |
| Port in use | Use different port |
| API key error | Add to .env |
| Models missing | Run train_models.py |
| Import error | pip install -r requirements.txt |
| CSS not loading | Hard refresh (Ctrl+F5) |
| Animations janky | Check GPU acceleration |
| API timeout | Check internet connection |

---

## ✨ Features Summary

### Core Features
- ✅ AI-powered nutrition recommendations
- ✅ ML calorie predictions
- ✅ ML protein predictions
- ✅ Gemini AI diet plans
- ✅ Scientific calculations (BMR/TDEE)
- ✅ Goal-based adjustments
- ✅ Macro breakdowns
- ✅ Water intake tracking

### UI/UX Features
- ✅ Glassmorphism design
- ✅ Dark futuristic theme
- ✅ Smooth animations
- ✅ Responsive layout
- ✅ Lucide icons
- ✅ Loading states
- ✅ Form validation
- ✅ Results dashboard

### Technical Features
- ✅ Flask backend
- ✅ Scikit-learn ML
- ✅ Google Gemini AI
- ✅ Jinja2 templating
- ✅ Vanilla JavaScript
- ✅ CSS variables
- ✅ Error handling
- ✅ Environment config

---

## 🎓 Educational Value

This project is perfect for:
- ✅ Portfolio building
- ✅ Final-year projects
- ✅ Full-stack learning
- ✅ ML integration examples
- ✅ UI/UX design showcase
- ✅ API integration patterns
- ✅ Best practices reference
- ✅ Production deployment

---

## 📖 Code Examples

### Getting Calories
```python
# In app.py
predicted_calories = models['calorie'].predict(X)[0]
```

### Form Submission
```javascript
// In script.js
fetch('/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(data)
})
```

### Styling with Variables
```css
/* In style.css */
background: var(--gradient-primary);
border: 1px solid var(--border);
color: var(--text);
```

---

## 📝 Version History

- **v1.0.0** (May 2024): Initial release
  - Core features complete
  - All integrations working
  - Production-ready UI
  - Full documentation

---

## 💡 Pro Tips

1. **Use dark mode** for better visual experience
2. **Test with real fitness data** for accurate predictions
3. **Generate multiple diet plans** for comparison
4. **Export results** for offline reference
5. **Share feedback** for improvements
6. **Monitor API usage** (Gemini quotas)
7. **Cache results** for faster access
8. **Update models** periodically with new data

---

```
🚀 Ready to launch your nutrition app? 🚀

Start with: python app.py
Access at: http://localhost:5000

Happy coding! 💻✨
```

---

**Quick Reference v1.0** | Last Updated: May 2024
