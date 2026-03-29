"""Diabetologist Agent — analyzes diabetes risk indicators."""


class DiabetologistAgent:
    name = "Diabetologist"

    def analyze(self, data: dict) -> dict:
        sugar = data.get("sugar_intake_g", 30)
        bmi = data.get("bmi", 22)
        age = data.get("age", 35)
        exercise = data.get("exercise_minutes", 30)
        fiber = data.get("fiber_g", 20)
        calories = data.get("calories", 2000)
        family_diabetes = data.get("family_diabetes", 0)
        water = data.get("water_ml", 2000)

        insights = []
        flags = []

        # Sugar intake
        WHO_DAILY_SUGAR_LIMIT = 50  # grams
        if sugar > WHO_DAILY_SUGAR_LIMIT * 2:
            flags.append("excessive_sugar")
            insights.append({
                "type": "risk",
                "title": "Very High Sugar Intake",
                "content": f"Consuming {sugar}g of sugar (WHO limit: 50g/day). This significantly raises insulin resistance risk. Cut out sugary drinks and processed foods.",
                "severity": "critical"
            })
        elif sugar > WHO_DAILY_SUGAR_LIMIT:
            flags.append("high_sugar")
            insights.append({
                "type": "warning",
                "title": "High Sugar Intake",
                "content": f"Sugar intake of {sugar}g exceeds WHO recommendation of 50g/day. Consider replacing sweets with fruits.",
                "severity": "warning"
            })

        # BMI
        if bmi > 30:
            flags.append("obese_bmi")
            insights.append({
                "type": "risk",
                "title": "Obesity Increases Diabetes Risk",
                "content": f"BMI of {bmi:.1f} (Obese range). Excess body fat causes insulin resistance. Target BMI 18.5–24.9 through diet and exercise.",
                "severity": "critical"
            })
        elif bmi > 25:
            flags.append("overweight_bmi")
            insights.append({
                "type": "warning",
                "title": "Overweight BMI",
                "content": f"BMI of {bmi:.1f} is in the overweight range. Reducing by 5-10% can dramatically lower diabetes risk.",
                "severity": "warning"
            })

        # Family history
        if family_diabetes:
            insights.append({
                "type": "info",
                "title": "Family History of Diabetes",
                "content": "Having a first-degree relative with diabetes increases your risk by 2-3x. Regular HbA1c testing is strongly recommended.",
                "severity": "info"
            })

        # Fiber
        if fiber < 15:
            insights.append({
                "type": "recommendation",
                "title": "Low Dietary Fiber",
                "content": f"Only {fiber}g of fiber today (target: 25-30g). Fiber slows glucose absorption and reduces diabetes risk dramatically.",
                "severity": "warning"
            })

        risk_score = min(100, max(0,
            (max(0, sugar - 30) * 0.6) +
            (max(0, bmi - 20) * 2.5) +
            (family_diabetes * 20) +
            (max(0, age - 40) * 0.6) +
            (max(0, 30 - exercise) * 0.4) +
            (max(0, 20 - fiber) * 0.8)
        ))

        summary = (
            f"Diabetes risk evaluated at {risk_score:.0f}/100. "
            + (f"Concerns: {', '.join(flags)}. " if flags else "Diabetes indicators look reasonable. ")
            + ("Priority: reduce sugar, increase fiber, manage weight." if flags else "Maintain current diet and exercise routine.")
        )

        return {
            "agent": self.name,
            "risk_score": round(risk_score, 1),
            "flags": flags,
            "insights": insights,
            "summary": summary
        }
