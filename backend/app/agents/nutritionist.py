"""Nutritionist Agent — analyzes diet quality and nutritional balance."""


class NutritionistAgent:
    name = "Nutritionist"

    def analyze(self, data: dict) -> dict:
        calories = data.get("calories", 2000)
        water = data.get("water_ml", 2000)
        sugar = data.get("sugar_intake_g", 30)
        fiber = data.get("fiber_g", 20)
        protein = data.get("protein_intake_g", 50)
        carbs = data.get("carbs_intake_g", 250)
        fat = data.get("fat_intake_g", 65)
        meal_desc = data.get("meal_description", "")
        bmi = data.get("bmi", 22)

        insights = []
        flags = []

        # Calorie check
        if calories > 3000:
            flags.append("excess_calories")
            insights.append({
                "type": "warning",
                "title": "Excess Calorie Intake",
                "content": f"You consumed {calories:.0f} kcal today. Aim for 1800-2200 kcal based on your activity level to prevent weight gain.",
                "severity": "warning"
            })
        elif calories < 1200:
            flags.append("insufficient_calories")
            insights.append({
                "type": "warning",
                "title": "Very Low Calorie Intake",
                "content": f"Only {calories:.0f} kcal detected. Severe restriction can cause muscle loss and nutrient deficiencies.",
                "severity": "warning"
            })

        # Water intake
        if water < 1500:
            flags.append("dehydrated")
            insights.append({
                "type": "alert",
                "title": "Dehydration Risk",
                "content": f"Only {water:.0f}ml of water today. Target is 2000-2500ml/day. Dehydration affects metabolism, energy, and kidney health.",
                "severity": "warning"
            })

        # Protein
        if protein < 40 and bmi < 25:
            flags.append("low_protein")
            insights.append({
                "type": "recommendation",
                "title": "Insufficient Protein",
                "content": f"Protein intake of {protein:.0f}g is low. Aim for 0.8-1g/kg body weight. Add eggs, legumes, or lean meat.",
                "severity": "info"
            })

        # Balanced macros
        total = (protein * 4) + (carbs * 4) + (fat * 9)
        if total > 100:
            protein_pct = round((protein * 4 / total) * 100, 1)
            carbs_pct = round((carbs * 4 / total) * 100, 1)
            fat_pct = round((fat * 9 / total) * 100, 1)

            if fat_pct > 40:
                flags.append("high_fat_diet")
                insights.append({
                    "type": "warning",
                    "title": "High Fat Diet",
                    "content": f"Fat makes up {fat_pct}% of your calories (ideal: 20-35%). Excess saturated fat raises CVD risk.",
                    "severity": "warning"
                })

        # Meal analysis (NLP keyword matching)
        meal_lower = meal_desc.lower()
        unhealthy_keywords = ["fried", "chips", "burger", "pizza", "soda", "cola", "candy", "junk"]
        healthy_keywords = ["salad", "vegetables", "fruits", "dal", "quinoa", "oats", "grilled", "steamed"]

        unhealthy_count = sum(1 for k in unhealthy_keywords if k in meal_lower)
        healthy_count = sum(1 for k in healthy_keywords if k in meal_lower)

        if unhealthy_count > healthy_count and unhealthy_count > 0:
            insights.append({
                "type": "recommendation",
                "title": "Diet Quality Concern",
                "content": f"Your meal description suggests processed/unhealthy foods. Try to include more vegetables, whole grains, and lean proteins.",
                "severity": "info"
            })
        elif healthy_count > 0:
            insights.append({
                "type": "info",
                "title": "Good Food Choices Detected",
                "content": "Your meal includes some healthy options. Keep it up!",
                "severity": "info"
            })

        risk_score = min(100, max(0,
            (max(0, sugar - 30) * 0.5) +
            (max(0, 1500 - water) * 0.02) +
            (unhealthy_count * 8) +
            (max(0, calories - 2200) * 0.02)
        ))

        summary = (
            f"Nutritional assessment complete. Risk score: {risk_score:.0f}/100. "
            + (f"Issues found: {', '.join(flags)}. " if flags else "Diet quality looks acceptable. ")
            + "Focus on hydration, fiber, and reducing processed foods."
        )

        return {
            "agent": self.name,
            "risk_score": round(risk_score, 1),
            "flags": flags,
            "insights": insights,
            "summary": summary
        }
