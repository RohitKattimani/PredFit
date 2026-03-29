"""
Conversational Logging Agent — NLP parser for natural language health input.
Extracts structured health data from free-text user messages.
"""
import re
from typing import Optional


FOOD_DATABASE = {
    # Indian foods
    "roti": {"calories": 120, "carbs": 18, "fiber": 2, "fat": 3},
    "paratha": {"calories": 250, "carbs": 30, "fat": 12, "fiber": 2},
    "dal": {"calories": 150, "carbs": 22, "protein": 9, "fiber": 6},
    "rice": {"calories": 200, "carbs": 45, "fiber": 1},
    "idli": {"calories": 80, "carbs": 17, "protein": 2, "fiber": 1},
    "sambar": {"calories": 90, "carbs": 12, "protein": 4, "fiber": 3},
    "paneer": {"calories": 300, "carbs": 10, "protein": 18, "fat": 22},
    "chicken": {"calories": 250, "protein": 30, "fat": 14},
    "biryani": {"calories": 450, "carbs": 55, "protein": 20, "fat": 18, "sugar": 5},
    "dosa": {"calories": 160, "carbs": 30, "protein": 4, "fat": 4},
    "upma": {"calories": 220, "carbs": 35, "protein": 5, "fat": 6},
    "poha": {"calories": 180, "carbs": 35, "protein": 4, "fat": 4},
    # Western / other
    "egg": {"calories": 155, "protein": 13, "fat": 11},
    "bread": {"calories": 130, "carbs": 25, "fiber": 2},
    "toast": {"calories": 130, "carbs": 25, "fiber": 2},
    "milk": {"calories": 120, "carbs": 12, "protein": 8, "fat": 5},
    "banana": {"calories": 90, "carbs": 23, "fiber": 3, "sugar": 12},
    "apple": {"calories": 80, "carbs": 21, "fiber": 4, "sugar": 15},
    "salad": {"calories": 50, "carbs": 8, "fiber": 4},
    "pizza": {"calories": 500, "carbs": 60, "fat": 22, "sugar": 8},
    "burger": {"calories": 550, "carbs": 42, "fat": 30, "protein": 25},
    "coffee": {"calories": 30, "sugar": 5},
    "chai": {"calories": 80, "sugar": 12},
    "juice": {"calories": 120, "sugar": 25, "carbs": 30},
    "oats": {"calories": 150, "carbs": 27, "fiber": 4, "protein": 5},
    "almonds": {"calories": 160, "fat": 14, "protein": 6, "fiber": 3},
}

EXERCISE_KEYWORDS = {
    "walk": 30, "walked": 30, "walking": 30,
    "jog": 60, "jogged": 60, "jogging": 60, "run": 60, "ran": 60, "running": 60,
    "gym": 50, "workout": 50, "exercise": 50, "yoga": 40, "cycling": 55,
    "swim": 70, "swimming": 70, "dance": 40, "dancing": 40,
    "hiit": 80, "cardio": 60,
}

WATER_PATTERNS = [
    (r"(\d+)\s*(?:glass|glasses)", lambda m: int(m.group(1)) * 250),
    (r"(\d+)\s*(?:litre|liter|l)\b", lambda m: int(m.group(1)) * 1000),
    (r"(\d+)\s*ml", lambda m: int(m.group(1))),
    (r"(\d+\.?\d*)\s*(?:litre|liter|l)\b", lambda m: float(m.group(1)) * 1000),
]

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "half": 0.5, "a": 1, "an": 1
}


class ConversationalAgent:
    name = "Conversational Agent"

    def parse(self, text: str) -> dict:
        """Parse natural language health input into structured data."""
        text_lower = text.lower().strip()
        result = {
            "intent": "unknown",
            "extracted": {},
            "confidence": 0.0,
            "response": "",
            "raw_input": text
        }

        # Replace number words
        for word, val in NUMBER_WORDS.items():
            text_lower = re.sub(r'\b' + word + r'\b', str(val), text_lower)

        # --- Food/Meal intent ---
        food_keywords = ["ate", "had", "eat", "lunch", "dinner", "breakfast", "snack", "meal", "drank"]
        if any(kw in text_lower for kw in food_keywords):
            result["intent"] = "food_log"
            extracted = self._extract_food(text_lower)
            result["extracted"].update(extracted)
            result["confidence"] = 0.85

            food_names = [f for f in FOOD_DATABASE if f in text_lower]
            cal = extracted.get("calories_intake", 0)
            result["response"] = (
                f"Logged your meal! Detected: {', '.join(food_names) if food_names else 'food items'}. "
                f"Estimated {cal:.0f} calories added to today's log."
            )

        # --- Exercise intent ---
        elif any(kw in text_lower for kw in EXERCISE_KEYWORDS):
            result["intent"] = "exercise_log"
            extracted = self._extract_exercise(text_lower)
            result["extracted"].update(extracted)
            result["confidence"] = 0.88

            mins = extracted.get("exercise_minutes", 30)
            ex_type = extracted.get("exercise_type", "exercise")
            result["response"] = f"Great! Logged {mins} minutes of {ex_type}. Keep it up! 💪"

        # --- Sleep intent ---
        elif any(kw in text_lower for kw in ["slept", "sleep", "woke", "hours of sleep"]):
            result["intent"] = "sleep_log"
            extracted = self._extract_sleep(text_lower)
            result["extracted"].update(extracted)
            result["confidence"] = 0.82

            hrs = extracted.get("sleep_hours", 0)
            result["response"] = (
                f"Logged {hrs}h of sleep. " +
                ("Great sleep! 😴" if hrs >= 7 else "Try to get at least 7 hours tonight. 🌙")
            )

        # --- Water intent ---
        elif any(kw in text_lower for kw in ["water", "drank", "drink", "hydrat"]):
            result["intent"] = "water_log"
            extracted = self._extract_water(text_lower)
            result["extracted"].update(extracted)
            result["confidence"] = 0.80

            ml = extracted.get("water_intake_ml", 0)
            result["response"] = f"Logged {ml:.0f}ml of water. 💧 Keep hydrating!"

        # --- Stress intent ---
        elif any(kw in text_lower for kw in ["stress", "anxious", "tired", "exhausted", "feeling"]):
            result["intent"] = "stress_log"
            stress = self._extract_stress(text_lower)
            result["extracted"]["stress_level"] = stress
            result["confidence"] = 0.75
            result["response"] = (
                f"Noted your stress level at {stress}/10. "
                + ("Take a deep breath — you've got this! 🧘" if stress <= 5 else "Consider a short walk or meditation break. 🌿")
            )

        else:
            result["intent"] = "general"
            result["response"] = (
                "I didn't catch specific health data from that. Try saying:\n"
                "• 'I had 2 rotis and dal for lunch'\n"
                "• 'Walked for 30 minutes'\n"
                "• 'Slept 7 hours last night'\n"
                "• 'Drank 3 glasses of water'"
            )

        result["extracted"]["log_source"] = "chat"
        result["extracted"]["raw_input"] = text
        result["extracted"]["meal_description"] = text if result["intent"] == "food_log" else ""

        return result

    def _extract_food(self, text: str) -> dict:
        total = {"calories_intake": 0, "carbs_intake_g": 0, "protein_intake_g": 0,
                 "fat_intake_g": 0, "fiber_intake_g": 0, "sugar_intake_g": 0}
        found = False

        for food, nutrients in FOOD_DATABASE.items():
            if food in text:
                # Detect quantity multiplier
                qty_match = re.search(r'(\d+\.?\d*)\s*' + food, text)
                qty = float(qty_match.group(1)) if qty_match else 1
                qty = min(qty, 5)  # cap multiplier

                for k, v in nutrients.items():
                    if k in total:
                        total[k] += v * qty
                found = True

        if not found:
            total["calories_intake"] = 350  # default estimate

        return {k: round(v, 1) for k, v in total.items()}

    def _extract_exercise(self, text: str) -> dict:
        exercise_type = "exercise"
        exercise_minutes = 30

        for kw, met_cal in EXERCISE_KEYWORDS.items():
            if kw in text:
                exercise_type = kw
                break

        time_match = re.search(r'(\d+\.?\d*)\s*(?:min|minute|minutes|mins)', text)
        if time_match:
            exercise_minutes = int(float(time_match.group(1)))
        else:
            hour_match = re.search(r'(\d+\.?\d*)\s*(?:hour|hours|hr|hrs)', text)
            if hour_match:
                exercise_minutes = int(float(hour_match.group(1)) * 60)

        return {
            "exercise_minutes": exercise_minutes,
            "exercise_type": exercise_type,
            "steps_count": exercise_minutes * 100  # rough estimate
        }

    def _extract_sleep(self, text: str) -> dict:
        time_match = re.search(r'(\d+\.?\d*)\s*(?:hour|hours|hr|hrs)?\s*(?:of\s+sleep|sleep)?', text)
        sleep_hours = float(time_match.group(1)) if time_match else 7.0
        sleep_hours = max(0, min(12, sleep_hours))

        quality = 7
        if any(w in text for w in ["well", "great", "deep", "good"]):
            quality = 8
        elif any(w in text for w in ["bad", "poor", "terrible", "couldn't"]):
            quality = 3

        return {"sleep_hours": sleep_hours, "sleep_quality": quality}

    def _extract_water(self, text: str) -> dict:
        for pattern, converter in WATER_PATTERNS:
            m = re.search(pattern, text)
            if m:
                return {"water_intake_ml": converter(m)}
        return {"water_intake_ml": 500}

    def _extract_stress(self, text: str) -> int:
        num_match = re.search(r'\b([1-9]|10)\b', text)
        if num_match:
            return int(num_match.group(1))
        if any(w in text for w in ["very stressed", "overwhelmed", "extremely"]):
            return 9
        if any(w in text for w in ["a bit", "slightly", "little"]):
            return 4
        if any(w in text for w in ["okay", "fine", "normal"]):
            return 5
        return 6


conversational_agent = ConversationalAgent()
