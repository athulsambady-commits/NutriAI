import os
import textwrap
try:
    import google.generativeai as gai
    GAI_AVAILABLE = True
except Exception:
    GAI_AVAILABLE = False

API_KEY = os.environ.get('GOOGLE_API_KEY')
if GAI_AVAILABLE and API_KEY:
    try:
        gai.configure(api_key=API_KEY)
    except Exception:
        pass

MODEL = 'gemini-1.5-flash'

def _build_prompt(user):
    prompt = f"""
You are an expert Indian gym nutritionist.
Create a practical, affordable, high-protein Indian diet plan tailored to the user.

User details:
- Age: {user.get('age')}
- Gender: {user.get('gender')}
- Weight: {user.get('weight')} kg
- Height: {user.get('height')} cm
- Goal: {user.get('goal')}
- Daily Calories: {user.get('calories')} kcal
- Daily Protein: {user.get('protein')} g

Produce:
- Breakfast
- Mid-morning snack
- Lunch
- Evening snack
- Pre-workout meal
- Post-workout meal
- Dinner
- Daily water intake suggestion
- Meal timings
- Kerala-specific suggestions (if applicable)
- Affordable swaps and grocery tips

Keep the plan concise, formatted with headings and bullet points.
"""
    return textwrap.dedent(prompt)


def generate_diet_plan(user):
    prompt = _build_prompt(user)
    if GAI_AVAILABLE and API_KEY:
        try:
            resp = gai.generate_text(model=MODEL, prompt=prompt, max_output_tokens=800)
            return resp.text
        except Exception:
            pass
    # Fallback deterministic plan when Gemini is not available
    plan = []
    plan.append(f"Breakfast: 2 eggs/egg bhurji + 2 multigrain chapatis or oats with milk — ~400 kcal, 25g protein")
    plan.append(f"Mid-morning: Greek yogurt or sprouted moong salad — 150 kcal, 10g protein")
    plan.append(f"Lunch: Grilled chicken/fish paneer + brown rice/quinoa + salad — 600 kcal, 35-40g protein")
    plan.append(f"Evening snack: Roasted chana or protein shake — 200 kcal, 20g protein")
    plan.append(f"Pre-workout: Banana + peanut butter or a small dosa — 150 kcal")
    plan.append(f"Post-workout: Whey shake or milk + banana — 200 kcal, 25g protein")
    plan.append(f"Dinner: Light dal/legume curry + chapati + veggies — 500 kcal, 30g protein")
    plan.append(f"Water: Aim for {user.get('calories')/1000*1.5:.1f} L/day (adjust as needed)")
    plan.append("Kerala tip: Include fish curry with less oil, steamed appam with egg for special workouts")
    return "\n\n".join(plan)
