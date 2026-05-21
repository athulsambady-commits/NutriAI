"""
Google Gemini AI Diet Planner
Production-ready version for Flask + Render deployment.
"""

import os
import re
import textwrap
from typing import Any

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# =========================================
# CONFIG
# =========================================

class Config:

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-1.5-flash"
    )


# =========================================
# MODEL FALLBACKS
# =========================================

DEFAULT_MODEL_FALLBACKS = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b"
]


# =========================================
# GEMINI DIET PLANNER
# =========================================

class GeminiDietPlanner:
    """
    Generates personalized diet plans
    using Google Gemini AI.
    """

    def __init__(
        self,
        api_key: str | None = None
    ):

        self.api_key = (
            api_key
            or Config.GEMINI_API_KEY
        )

        self.enabled = bool(
            self.api_key
        )

        self.model_names = [
            Config.GEMINI_MODEL,
            *DEFAULT_MODEL_FALLBACKS
        ]

        # Remove duplicates
        seen = set()

        self.model_names = [
            m for m in self.model_names
            if m and not (
                m in seen
                or seen.add(m)
            )
        ]

        self._genai_client = None

        self._legacy_configured = False

        if not self.enabled:
            return

        # Try latest SDK
        try:

            from google import genai

            self._genai_client = genai.Client(
                api_key=self.api_key
            )

            self._sdk = "genai"

        except ImportError:

            self._init_legacy_sdk()

    # =====================================
    # LEGACY SDK
    # =====================================

    def _init_legacy_sdk(self):

        try:

            import google.generativeai as genai_legacy

            genai_legacy.configure(
                api_key=self.api_key
            )

            self._legacy_genai = genai_legacy

            self._legacy_configured = True

            self._sdk = "legacy"

        except ImportError:

            self.enabled = False

    # =====================================
    # CLEAN AI RESPONSE
    # =====================================

    def _clean_response(
        self,
        text: str
    ) -> str:

        if not text:
            return ""

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()

        return text

    # =====================================
    # SAFE FLOAT CONVERTER
    # =====================================

    @staticmethod
    def _safe_float(
        value: Any,
        default: float
    ) -> float:

        try:

            if value is None:
                return default

            return float(value)

        except (
            TypeError,
            ValueError
        ):

            return default

    # =====================================
    # BUILD PROMPT
    # =====================================

    def _build_prompt(
        self,
        profile: dict[str, Any],
        food_habits: str | None = None,
        existing_plan: str | None = None,
    ) -> str:

        calories = self._safe_float(
            profile.get("calories"),
            2000
        )

        protein = self._safe_float(
            profile.get("protein"),
            120
        )

        goal = profile.get(
            "goal",
            "Maintenance"
        )

        workout_type = profile.get(
            "workout_type",
            "Mixed"
        )

        experience = profile.get(
            "experience_level",
            "Intermediate"
        )

        frequency = profile.get(
            "workout_frequency",
            3
        )

        session_mins = profile.get(
            "session_duration",
            60
        )

        water_l = self._safe_float(
            profile.get("water_intake"),
            2.5
        )

        bmi = profile.get("bmi")

        bmi_value = self._safe_float(
            bmi,
            -1
        )

        bmi_line = ""

        if bmi_value >= 0:

            bmi_line = (
                f"- BMI: {bmi_value:.1f}\n"
            )

        # Food habits block
        food_habits_block = ""

        if food_habits:

            food_habits_block = textwrap.dedent(f"""
                FOOD HABITS / PREFERENCES:
                {food_habits}
            """).strip()

        # Existing plan block
        existing_plan_block = ""

        if existing_plan:

            existing_plan_block = textwrap.dedent(f"""
                CURRENT DIET PLAN:
                {existing_plan}
            """).strip()

        extra_context = "\n\n".join(
            block for block in [
                food_habits_block,
                existing_plan_block
            ]
            if block
        )

        strict_rules = ""

        if food_habits:

            strict_rules = textwrap.dedent("""
                STRICT RULES:
                - Follow food restrictions exactly.
                - If vegetarian, never include meat/fish/chicken.
                - Avoid disliked foods.
                - Suggest practical alternatives.
            """).strip()

        # Final Prompt
        prompt = f"""
You are an expert gym nutritionist and sports dietitian.

Create a personalized Indian gym diet plan.

USER PROFILE:
- Age: {profile.get('age')} years
- Gender: {profile.get('gender')}
- Weight: {profile.get('weight')} kg
- Height: {profile.get('height')} cm
{bmi_line}- Goal: {goal}
- Workout Type: {workout_type}
- Workout Frequency: {frequency} days/week
- Session Duration: {session_mins} minutes
- Experience Level: {experience}
- Daily Calories Target: {calories:.0f} kcal
- Daily Protein Target: {protein:.0f} grams
- Daily Water Intake: {water_l} liters

REQUIREMENTS:
1. Create a full-day meal plan.
2. Include meal timings.
3. Include:
   - Breakfast
   - Mid-morning snack
   - Lunch
   - Evening snack
   - Pre-workout meal
   - Post-workout meal
   - Dinner
4. Mention calories and protein for meals.
5. Suggest affordable Indian foods.
6. Include Kerala food options if suitable.
7. High protein focus.
8. Easy to cook meals.
9. Add hydration schedule.
10. Add workout nutrition tips.
11. Add a short grocery shopping list.
12. Tailor diet for the user's goal.

{extra_context}

{strict_rules}

FORMAT RULES:
- Use markdown headings.
- Use bullet points.
- Keep response clean and readable.
- Be practical and concise.
"""

        return textwrap.dedent(
            prompt
        ).strip()

    # =====================================
    # NEW SDK CALL
    # =====================================

    def _call_genai_sdk(
        self,
        prompt: str
    ) -> str | None:

        if not self._genai_client:
            return None

        last_error = None

        for model_name in self.model_names:

            try:

                response = (
                    self._genai_client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                )

                text = getattr(
                    response,
                    "text",
                    None
                )

                if text and text.strip():

                    return text.strip()

            except Exception as exc:

                last_error = exc

                print(
                    f"[Gemini Error] "
                    f"{model_name}: {str(exc)}"
                )

        if last_error:

            print(
                f"[Gemini] All models failed: "
                f"{last_error}"
            )

        return None

    # =====================================
    # LEGACY SDK CALL
    # =====================================

    def _call_legacy_sdk(
        self,
        prompt: str
    ) -> str | None:

        if not self._legacy_configured:
            return None

        last_error = None

        for model_name in self.model_names:

            try:

                model = (
                    self._legacy_genai.GenerativeModel(
                        model_name
                    )
                )

                response = model.generate_content(
                    prompt
                )

                text = getattr(
                    response,
                    "text",
                    None
                )

                if text and text.strip():

                    return text.strip()

            except Exception as exc:

                last_error = exc

                print(
                    f"[Legacy Gemini Error] "
                    f"{model_name}: {str(exc)}"
                )

        if last_error:

            print(
                f"[Legacy Gemini] "
                f"All models failed: "
                f"{last_error}"
            )

        return None

    # =====================================
    # MAIN GENERATOR
    # =====================================

    def generate_diet_plan(
        self,
        profile: dict[str, Any],
        food_habits: str | None = None,
        existing_plan: str | None = None,
    ) -> dict[str, str]:

        prompt = self._build_prompt(
            profile=profile,
            food_habits=food_habits,
            existing_plan=existing_plan,
        )

        if self.enabled:

            text = None

            if self._genai_client:

                text = self._call_genai_sdk(
                    prompt
                )

            elif self._legacy_configured:

                text = self._call_legacy_sdk(
                    prompt
                )

            if text:

                cleaned_text = (
                    self._clean_response(text)
                )

                return {
                    "plan": cleaned_text,
                    "source": "gemini"
                }

        # Fallback plan
        plan = self.get_default_diet_plan(
            profile,
            food_habits
        )

        return {
            "plan": plan,
            "source": "fallback"
        }

    # =====================================
    # FALLBACK DIET PLAN
    # =====================================

    @staticmethod
    def get_default_diet_plan(
        profile: dict[str, Any],
        food_habits: str | None = None
    ) -> str:

        calories = 2000
        protein = 120

        try:

            calories = float(
                profile.get(
                    "calories",
                    2000
                )
            )

            protein = float(
                profile.get(
                    "protein",
                    120
                )
            )

        except Exception:
            pass

        goal = profile.get(
            "goal",
            "Maintenance"
        )

        habits = (
            food_habits or ""
        ).lower()

        is_veg = bool(
            re.search(
                r"\b(veg|vegetarian|pure veg)\b",
                habits
            )
        )

        if is_veg:

            protein_source = (
                "paneer/tofu/soy chunks"
            )

        else:

            protein_source = (
                "chicken/fish/eggs/paneer"
            )

        return f"""
# Personalized Diet Plan

## Goal
{goal}

## Daily Targets
- Calories: {calories:.0f} kcal
- Protein: {protein:.0f} g

## Breakfast
- Oats with milk
- Banana
- {protein_source}

## Mid-Morning Snack
- Protein shake
- Dry fruits

## Lunch
- Brown rice
- Dal
- Salad
- {protein_source}

## Pre-Workout
- Banana
- Black coffee

## Post-Workout
- Whey protein shake
- Fruits

## Dinner
- Roti
- Mixed vegetables
- {protein_source}

## Water Intake
- 3 to 4 liters daily

## Tips
- Maintain protein intake
- Avoid junk food
- Sleep 7-8 hours
- Stay hydrated
"""

# =========================================
# SINGLETON INSTANCE
# =========================================

_planner_instance = None


def get_diet_planner():

    global _planner_instance

    if _planner_instance is None:

        _planner_instance = GeminiDietPlanner()

    return _planner_instance


def create_diet_planner(
    api_key: str | None = None
):

    return GeminiDietPlanner(
        api_key=api_key
    )