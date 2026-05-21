"""
Google Gemini AI diet plan generation.
Uses the google-genai SDK when available, with legacy SDK fallback.
"""

import os
import textwrap
from typing import Any
import re

from dotenv import load_dotenv

from config import Config

load_dotenv()

# Preferred models (tried in order until one succeeds)
DEFAULT_MODEL_FALLBACKS = [
    'gemini-2.0-flash',
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
]


class GeminiDietPlanner:
    """Generates personalized diet plans via Google Gemini."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or Config.GEMINI_API_KEY or os.getenv('GEMINI_API_KEY')
        self.enabled = bool(self.api_key)
        self.model_names = [Config.GEMINI_MODEL, *DEFAULT_MODEL_FALLBACKS]
        # Deduplicate while preserving order
        seen = set()
        self.model_names = [m for m in self.model_names if m and not (m in seen or seen.add(m))]

        self._genai_client = None
        self._legacy_configured = False

        if not self.enabled:
            return

        try:
            from google import genai

            self._genai_client = genai.Client(api_key=self.api_key)
            self._sdk = 'genai'
        except ImportError:
            self._init_legacy_sdk()

    def _init_legacy_sdk(self) -> None:
        try:
            import google.generativeai as genai_legacy

            genai_legacy.configure(api_key=self.api_key)
            self._legacy_genai = genai_legacy
            self._legacy_configured = True
            self._sdk = 'legacy'
        except ImportError:
            self.enabled = False

    def _build_prompt(
        self,
        profile: dict[str, Any],
        food_habits: str | None = None,
        existing_plan: str | None = None,
    ) -> str:
        def _safe_float(value: Any, default: float) -> float:
            try:
                if value is None:
                    return default
                return float(value)
            except (TypeError, ValueError):
                return default

        calories = _safe_float(profile.get('calories'), 2000)
        protein = _safe_float(profile.get('protein'), 120)
        goal = profile.get('goal', 'Maintenance')
        workout_type = profile.get('workout_type', 'Mixed')
        experience = profile.get('experience_level', 'Intermediate')
        frequency = profile.get('workout_frequency', 3)
        session_mins = profile.get('session_duration', 60)
        water_l = _safe_float(profile.get('water_intake'), 2.5)
        bmi = profile.get('bmi')

        bmi_value = _safe_float(bmi, -1)
        bmi_line = f"- BMI: {bmi_value:.1f}\n" if bmi_value >= 0 else ""

        food_habits_block = ""
        if food_habits:
            food_habits_block = textwrap.dedent(f"""
                FOOD HABITS / PREFERENCES FROM USER:
                {food_habits}
            """).strip()

        existing_plan_block = ""
        if existing_plan:
            existing_plan_block = textwrap.dedent(f"""
                CURRENT DIET PLAN TO IMPROVE:
                {existing_plan}
            """).strip()

        extra_context = "\n\n".join(
            block for block in [food_habits_block, existing_plan_block] if block
        )

        strict_rules = ""
        if food_habits:
            strict_rules = textwrap.dedent("""
                STRICT COMPLIANCE RULES:
                - Treat user food habits/restrictions as mandatory constraints.
                - If user says vegetarian/veg, do NOT include chicken, fish, egg, meat, or seafood.
                - If any user dislike/allergy is mentioned, never include those foods.
                - If the current plan violates constraints, replace those items with compliant alternatives.
                - Return only the corrected plan.
            """).strip()

        return textwrap.dedent(f"""
            You are a professional gym nutritionist. Create a practical daily diet plan.

            USER PROFILE:
            - Age: {profile.get('age')} years
            - Gender: {profile.get('gender')}
            - Weight: {profile.get('weight')} kg
            - Height: {profile.get('height')} cm
            {bmi_line}- Fitness goal: {goal}
            - Workout: {workout_type}, {frequency} days/week, {session_mins} min sessions
            - Experience: {experience}
            - Daily calorie target: {calories:.0f} kcal
            - Daily protein target: {protein:.0f} g
            - Water intake: {water_l} L/day

            REQUIREMENTS:
            1. Full day plan with meal timings (breakfast through dinner).
            2. High-protein focus (at least {protein:.0f} g total).
            3. Indian cuisine with Kerala-friendly options where relevant.
            4. Affordable, easy-to-cook ingredients.
            5. Pre-workout and post-workout meals.
            6. Per-meal calories and macros (protein/carbs/fats).
            7. Hydration schedule and a short shopping list.
            8. Tailor portions and tips specifically for "{goal}".
            9. Respect the user's food habits, likes/dislikes, schedule, and restrictions if provided.

            {extra_context}
            {strict_rules}

            Format with clear headings and bullet points. Be concise but complete.
        """).strip()

    def _call_genai_sdk(self, prompt: str) -> str | None:
        if not self._genai_client:
            return None

        last_error = None
        for model_name in self.model_names:
            try:
                response = self._genai_client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                text = getattr(response, 'text', None)
                if text and text.strip():
                    return text.strip()
            except Exception as exc:
                last_error = exc
                print(f"[Gemini] Model {model_name} failed: {exc}")

        if last_error:
            print(f"[Gemini] All models failed. Last error: {last_error}")
        return None

    def _call_legacy_sdk(self, prompt: str) -> str | None:
        if not self._legacy_configured:
            return None

        last_error = None
        for model_name in self.model_names:
            try:
                model = self._legacy_genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                text = getattr(response, 'text', None)
                if text and text.strip():
                    return text.strip()
            except Exception as exc:
                last_error = exc
                print(f"[Gemini legacy] Model {model_name} failed: {exc}")

        if last_error:
            print(f"[Gemini legacy] All models failed. Last error: {last_error}")
        return None

    def generate_diet_plan(
        self,
        profile: dict[str, Any],
        food_habits: str | None = None,
        existing_plan: str | None = None,
    ) -> dict[str, str]:
        """
        Generate a diet plan from a user profile dict.

        Returns:
            dict with keys: plan (str), source ('gemini' | 'fallback')
        """
        prompt = self._build_prompt(
            profile=profile,
            food_habits=food_habits,
            existing_plan=existing_plan,
        )

        if self.enabled:
            text = None
            if self._genai_client:
                text = self._call_genai_sdk(prompt)
            elif self._legacy_configured:
                text = self._call_legacy_sdk(prompt)

            if text:
                return {'plan': text, 'source': 'gemini'}

        plan = self.get_default_diet_plan(profile, food_habits=food_habits)
        return {'plan': plan, 'source': 'fallback'}

    @staticmethod
    def get_default_diet_plan(profile: dict[str, Any], food_habits: str | None = None) -> str:
        """Fallback plan when Gemini is unavailable or fails."""
        def _safe_float(value: Any, default: float) -> float:
            try:
                if value is None:
                    return default
                return float(value)
            except (TypeError, ValueError):
                return default

        calories = _safe_float(profile.get('calories'), 2000)
        protein = _safe_float(profile.get('protein'), 120)
        goal = profile.get('goal', 'Maintenance')
        gender = profile.get('gender', 'Male')
        water_l = _safe_float(profile.get('water_intake'), 2.5)

        habits = (food_habits or "").lower()
        is_veg = bool(re.search(r"\b(veg|vegetarian|pure veg|no non[- ]?veg)\b", habits))

        if is_veg:
            protein_lunch = "Paneer curry (150g) or soy chunks masala (100g) — ~260 kcal, 28g protein"
            protein_dinner = "Paneer tikka/tofu stir-fry (150g) — ~230 kcal, 24g protein"
            protein_breakfast = "Moong chilla or paneer bhurji — ~220 kcal, 18g protein"
            shopping_protein = "paneer, tofu, soy chunks, eggs optional, dal, whey"
            kerala_tip = "Kerala option: kadala curry, avial, and appam with paneer/tofu for training days."
        else:
            protein_lunch = "Grilled chicken/fish or paneer curry (150g) — ~220 kcal, 28g protein"
            protein_dinner = "Grilled paneer or fish (150g) — ~230 kcal, 24g protein"
            protein_breakfast = "2 boiled eggs or paneer bhurji — ~140 kcal, 12g protein"
            shopping_protein = "chicken, fish, eggs, paneer, dal, whey"
            kerala_tip = "Kerala option: fish curry (light oil), appam with egg on heavy training days."

        return textwrap.dedent(f"""
            PERSONALIZED NUTRITION PLAN (offline fallback)
            Goal: {goal} | Target: {calories:.0f} kcal, {protein:.0f} g protein/day

            BREAKFAST (7:00 AM)
            - Vegetable upma or oats with milk (150g) — ~250 kcal, 10g protein
            - {protein_breakfast}
            - Green tea

            MID-MORNING (10:00 AM)
            - Protein shake (whey + milk) or Greek yogurt — ~200 kcal, 20g protein
            - 1 banana — ~90 kcal

            LUNCH (1:00 PM)
            - Brown rice (150g cooked) — ~195 kcal, 4g protein
            - {protein_lunch}
            - Mixed salad — ~80 kcal

            PRE-WORKOUT (3:00 PM)
            - Rice cakes with honey or 1 dosa — ~150 kcal

            POST-WORKOUT (within 45 min)
            - Protein shake + banana — ~250 kcal, 25g protein

            DINNER (8:00 PM)
            - 2 roti + dal (1 cup) + {protein_dinner} — ~460 kcal, 30g protein
            - Cucumber raita — ~40 kcal

            HYDRATION
            - Target: {water_l} L/day (more on training days)
            - 500 ml before workout, 250 ml every 15–20 min during, 500 ml after

            NOTES FOR {goal.upper()}
            - Hit protein at every meal; adjust rice/roti portions for {goal.lower()}.
            - {kerala_tip}
            - Meal prep 2–3 days ahead for consistency.

            SHOPPING LIST
            - Protein: {shopping_protein}
            - Carbs: rice, oats, roti flour
            - Produce: banana, spinach, cucumber, tomato
            - Pantry: milk, yogurt, honey, olive oil

            Profile: {gender}, {profile.get('weight', 70)} kg — plan generated without live AI.
        """).strip()


_planner_instance: GeminiDietPlanner | None = None


def get_diet_planner() -> GeminiDietPlanner:
    """Reuse a single planner instance across requests."""
    global _planner_instance
    if _planner_instance is None:
        _planner_instance = GeminiDietPlanner()
    return _planner_instance


def create_diet_planner(api_key: str | None = None) -> GeminiDietPlanner:
    return GeminiDietPlanner(api_key=api_key)
