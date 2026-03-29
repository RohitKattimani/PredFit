"""Lifestyle Coach Agent — analyzes activity, stress, and behavioral patterns."""


class LifestyleCoachAgent:
    name = "Lifestyle Coach"

    def analyze(self, data: dict) -> dict:
        exercise = data.get("exercise_minutes", 30)
        steps = data.get("steps_count", 5000)
        stress = data.get("stress_level", 5)
        mood = data.get("mood", "neutral")
        smoking = data.get("smoking", 0)
        alcohol = data.get("alcohol_units", 0)
        bmi = data.get("bmi", 22)
        age = data.get("age", 35)

        insights = []
        flags = []

        # Activity
        if steps < 3000:
            flags.append("sedentary")
            insights.append({
                "type": "alert",
                "title": "Sedentary Lifestyle Detected",
                "content": f"Only {steps} steps today. WHO recommends 7,000-10,000 steps/day. Sedentary behavior is linked to 30+ chronic diseases.",
                "severity": "critical"
            })
        elif steps < 7000:
            insights.append({
                "type": "recommendation",
                "title": "Increase Daily Steps",
                "content": f"You took {steps} steps. Try to reach 7,000+ steps with a 20-min walk after meals.",
                "severity": "info"
            })

        if exercise < 20:
            flags.append("low_exercise")
            insights.append({
                "type": "warning",
                "title": "Insufficient Exercise",
                "content": "Less than 20 min of exercise detected. Even a 30-min daily walk can reduce all-cause mortality by 35%.",
                "severity": "warning"
            })

        # Stress
        if stress >= 8:
            flags.append("high_stress")
            insights.append({
                "type": "alert",
                "title": "High Stress Level",
                "content": f"Stress level {stress}/10 is very high. Chronic stress elevates cortisol and increases risk of HTN, diabetes, and depression. Try 10 minutes of meditation or deep breathing.",
                "severity": "critical"
            })
        elif stress >= 6:
            insights.append({
                "type": "warning",
                "title": "Elevated Stress",
                "content": f"Stress at {stress}/10. Practice mindfulness, take short breaks, and prioritize sleep to manage cortisol levels.",
                "severity": "warning"
            })

        # Mood
        if mood in ["anxious", "depressed", "sad"]:
            insights.append({
                "type": "info",
                "title": "Mood Worth Monitoring",
                "content": f"You reported feeling {mood}. Mental health directly impacts physical health outcomes. Consider speaking to a counselor or practicing journaling.",
                "severity": "info"
            })

        # Substance use
        if alcohol > 2:
            flags.append("excess_alcohol")
            insights.append({
                "type": "warning",
                "title": "Excess Alcohol",
                "content": f"{alcohol} units of alcohol recorded. Limit to 1-2 units/day. Excess alcohol raises blood pressure and liver disease risk.",
                "severity": "warning"
            })

        risk_score = min(100, max(0,
            (max(0, 7000 - steps) * 0.005) +
            (stress * 4) +
            (max(0, 30 - exercise) * 0.5) +
            (smoking * 2) +
            (alcohol * 4)
        ))

        summary = (
            f"Lifestyle risk assessed at {risk_score:.0f}/100. "
            + (f"Flags: {', '.join(flags)}. " if flags else "Good lifestyle habits overall. ")
            + "Focus on consistency in exercise and stress management."
        )

        return {
            "agent": self.name,
            "risk_score": round(risk_score, 1),
            "flags": flags,
            "insights": insights,
            "summary": summary
        }
