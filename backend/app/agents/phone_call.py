"""
Phone Call Agent — Simulates an autonomous outbound health check-in call.
In production, this would integrate with Twilio/VAPI for real voice calls.
"""
import random
from datetime import datetime


CALL_SCRIPTS = [
    {
        "question": "What did you eat for breakfast today?",
        "field": "meal_description",
        "follow_up": "How much water have you had so far today?"
    },
    {
        "question": "Did you exercise or go for a walk today?",
        "field": "exercise_type",
        "follow_up": "For roughly how many minutes?"
    },
    {
        "question": "How many hours did you sleep last night?",
        "field": "sleep_hours",
        "follow_up": "How would you rate the quality of your sleep on a scale of 1 to 10?"
    },
    {
        "question": "How stressed are you feeling today on a scale of 1 to 10?",
        "field": "stress_level",
        "follow_up": "What's the main source of your stress?"
    },
]

SAMPLE_RESPONSES = {
    "breakfast": [
        ("I had 2 eggs and toast with orange juice", {"meal_description": "eggs toast orange juice", "calories_intake": 420, "sugar_intake_g": 25}),
        ("Just had idli and sambar", {"meal_description": "idli sambar", "calories_intake": 280, "sugar_intake_g": 5}),
        ("I skipped breakfast", {"meal_description": "skipped", "calories_intake": 0}),
        ("Had parathas with butter and chai", {"meal_description": "paratha butter chai", "calories_intake": 520, "sugar_intake_g": 15, "fat_intake_g": 22}),
    ],
    "exercise": [
        ("Yes, I jogged for about 30 minutes", {"exercise_type": "jogging", "exercise_minutes": 30, "steps_count": 4200}),
        ("Just a short walk to the office", {"exercise_type": "walking", "exercise_minutes": 15, "steps_count": 2000}),
        ("No, I didn't exercise today", {"exercise_type": "none", "exercise_minutes": 0}),
        ("I did yoga for 45 minutes", {"exercise_type": "yoga", "exercise_minutes": 45}),
    ],
    "sleep": [
        ("About 6 hours", {"sleep_hours": 6.0}),
        ("I got 7 and a half hours", {"sleep_hours": 7.5}),
        ("Only 4 hours, couldn't sleep well", {"sleep_hours": 4.0, "sleep_quality": 3}),
        ("Around 8 hours, slept really well", {"sleep_hours": 8.0, "sleep_quality": 8}),
    ],
    "stress": [
        ("About a 7, work has been intense", {"stress_level": 7}),
        ("Maybe a 4, feeling okay today", {"stress_level": 4}),
        ("High, probably a 9", {"stress_level": 9}),
        ("Fairly low, maybe 3", {"stress_level": 3}),
    ]
}


class PhoneCallAgent:
    name = "Phone Call Agent"

    def simulate_call(self, user_name: str = "there") -> dict:
        """Simulate an autonomous outbound health check-in call."""
        now = datetime.now()

        transcript = []
        extracted_data = {}

        # Opening
        transcript.append({
            "speaker": "AI Agent",
            "text": f"Hello {user_name}! This is your health check-in call from HealthGuard AI. This will just take 2 minutes. Is now a good time?"
        })
        transcript.append({
            "speaker": "User",
            "text": "Yes, go ahead."
        })

        # Meal check
        meal_resp, meal_data = random.choice(SAMPLE_RESPONSES["breakfast"])
        transcript.append({
            "speaker": "AI Agent",
            "text": "Great! What did you eat today — any meals you've had so far?"
        })
        transcript.append({"speaker": "User", "text": meal_resp})
        extracted_data.update(meal_data)
        transcript.append({
            "speaker": "AI Agent",
            "text": f"Got it, I've logged that. And how much water have you had today?"
        })
        transcript.append({"speaker": "User", "text": "About 1 litre so far."})
        extracted_data["water_intake_ml"] = 1000

        # Exercise check
        ex_resp, ex_data = random.choice(SAMPLE_RESPONSES["exercise"])
        transcript.append({
            "speaker": "AI Agent",
            "text": "Have you done any exercise or physical activity today?"
        })
        transcript.append({"speaker": "User", "text": ex_resp})
        extracted_data.update(ex_data)

        # Sleep check
        sleep_resp, sleep_data = random.choice(SAMPLE_RESPONSES["sleep"])
        transcript.append({
            "speaker": "AI Agent",
            "text": "How many hours did you sleep last night?"
        })
        transcript.append({"speaker": "User", "text": sleep_resp})
        extracted_data.update(sleep_data)

        # Stress check
        stress_resp, stress_data = random.choice(SAMPLE_RESPONSES["stress"])
        transcript.append({
            "speaker": "AI Agent",
            "text": "On a scale of 1 to 10, how stressed are you feeling today?"
        })
        transcript.append({"speaker": "User", "text": stress_resp})
        extracted_data.update(stress_data)

        # Closing
        risk_hint = "healthy" if extracted_data.get("stress_level", 5) < 7 else "a bit high"
        transcript.append({
            "speaker": "AI Agent",
            "text": f"Thank you! I've logged all your data. Your stress level seems {risk_hint} today. "
                    f"Your updated health report will be available in the app. Have a healthy day!"
        })
        transcript.append({"speaker": "User", "text": "Thank you, bye!"})

        extracted_data["log_source"] = "phone_call"
        extracted_data["raw_input"] = " | ".join([t["text"] for t in transcript if t["speaker"] == "User"])

        return {
            "agent": self.name,
            "call_time": str(now),
            "duration_seconds": random.randint(90, 180),
            "transcript": transcript,
            "extracted_data": extracted_data,
            "status": "completed"
        }


phone_call_agent = PhoneCallAgent()
