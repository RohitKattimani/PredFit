"""Recommendation Agent — generates personalized health recommendations."""


class RecommendationAgent:
    name = "Recommendation"

    def generate(self, user_data: dict, risk_scores: dict, consensus: dict) -> list:
        recommendations = []
        bmi = user_data.get("bmi", 22)
        sleep = user_data.get("sleep_hours", 7)
        exercise = user_data.get("exercise_minutes", 30)
        sugar = user_data.get("sugar_intake_g", 30)
        water = user_data.get("water_ml", 2000)
        stress = user_data.get("stress_level", 5)
        steps = user_data.get("steps_count", 5000)
        fiber = user_data.get("fiber_g", 20)
        smoking = user_data.get("smoking", 0)

        diab = risk_scores.get("diabetes", 0)
        htn = risk_scores.get("hypertension", 0)
        cvd = risk_scores.get("cvd", 0)
        obesity = risk_scores.get("obesity", 0)
        sleep_risk = risk_scores.get("sleep_disorder", 0)

        # Diet recommendations
        if diab > 45 or sugar > 50:
            recommendations.append({
                "category": "diet",
                "title": "Reduce Sugar Intake",
                "description": (
                    "Your sugar intake and diabetes risk are elevated. Switch to low-glycemic foods:\n"
                    "• Replace white rice with brown rice or quinoa\n"
                    "• Avoid sugary drinks — drink water or unsweetened green tea\n"
                    "• Snack on nuts, seeds, or low-sugar fruits (berries, apples)\n"
                    "• Read food labels and aim for <50g added sugar/day"
                ),
                "priority": "high",
                "agent_source": "recommendation+diabetologist"
            })

        if fiber < 20:
            recommendations.append({
                "category": "diet",
                "title": "Increase Dietary Fiber",
                "description": (
                    "Low fiber intake is linked to higher diabetes and CVD risk:\n"
                    "• Add a serving of legumes (dal, lentils, chickpeas) daily\n"
                    "• Choose whole grain bread/roti over refined flour\n"
                    "• Eat at least 2 servings of vegetables with each meal\n"
                    "• Target: 25–30g of fiber per day"
                ),
                "priority": "medium",
                "agent_source": "recommendation+nutritionist"
            })

        if water < 1500:
            recommendations.append({
                "category": "diet",
                "title": "Improve Hydration",
                "description": (
                    "You're not drinking enough water. Dehydration impacts every organ:\n"
                    "• Keep a 1L water bottle visible at your desk\n"
                    "• Set hourly reminders to drink water\n"
                    "• Eat water-rich foods: cucumber, watermelon, oranges\n"
                    "• Target: minimum 2000ml (8 glasses) per day"
                ),
                "priority": "medium",
                "agent_source": "recommendation+nutritionist"
            })

        # Exercise recommendations
        if cvd > 40 or exercise < 30:
            recommendations.append({
                "category": "exercise",
                "title": "30-Minute Daily Cardio",
                "description": (
                    "Cardiovascular exercise is the single most powerful preventive tool:\n"
                    "• Week 1-2: Brisk walking 30 min/day\n"
                    "• Week 3-4: Add jogging intervals (2 min jog, 3 min walk)\n"
                    "• Alternative: Cycling, swimming, or dancing\n"
                    "• Target: 150 min/week of moderate intensity cardio"
                ),
                "priority": "high" if cvd > 60 else "medium",
                "agent_source": "recommendation+cardiologist"
            })

        if steps < 7000:
            recommendations.append({
                "category": "exercise",
                "title": "Increase Daily Steps",
                "description": (
                    "Simple step increases have huge health benefits:\n"
                    "• Take stairs instead of elevator\n"
                    "• Walk during phone calls\n"
                    "• Park farther away from entrances\n"
                    "• 10-minute walks after each meal\n"
                    "• Goal: 8,000-10,000 steps/day"
                ),
                "priority": "medium",
                "agent_source": "recommendation+lifestyle_coach"
            })

        if obesity > 50 or bmi > 28:
            recommendations.append({
                "category": "exercise",
                "title": "Weight Management Plan",
                "description": (
                    "Reducing weight by even 5-10% dramatically lowers disease risk:\n"
                    "• Combine cardio + strength training 3x/week\n"
                    "• Use a smaller plate to control portions\n"
                    "• Eat slowly and mindfully\n"
                    "• Sleep 7-8h — poor sleep promotes weight gain\n"
                    "• Track meals in this app to stay accountable"
                ),
                "priority": "high",
                "agent_source": "recommendation+lifestyle_coach"
            })

        # Sleep recommendations
        if sleep_risk > 40 or sleep < 6.5:
            recommendations.append({
                "category": "sleep",
                "title": "Optimize Your Sleep",
                "description": (
                    "Quality sleep is foundational to all disease prevention:\n"
                    "• Set a consistent sleep and wake time (even weekends)\n"
                    "• No screens 1 hour before bedtime\n"
                    "• Keep bedroom cool (18–20°C) and dark\n"
                    "• Avoid caffeine after 2pm\n"
                    "• Try 4-7-8 breathing for faster sleep onset"
                ),
                "priority": "high" if sleep < 5 else "medium",
                "agent_source": "recommendation+sleep_specialist"
            })

        # Stress recommendations
        if stress > 6:
            recommendations.append({
                "category": "lifestyle",
                "title": "Stress Reduction Protocol",
                "description": (
                    "Chronic stress is a root cause of most lifestyle diseases:\n"
                    "• 10 min of mindfulness meditation daily (try Headspace or Calm)\n"
                    "• Take 5-minute breaks every hour at work\n"
                    "• Practice gratitude journaling before bed\n"
                    "• Limit news/social media to 30 min/day\n"
                    "• Connect with friends/family — social bonding reduces cortisol"
                ),
                "priority": "high" if stress > 8 else "medium",
                "agent_source": "recommendation+lifestyle_coach"
            })

        # Smoking
        if smoking > 0:
            recommendations.append({
                "category": "lifestyle",
                "title": "Quit Smoking — Highest Priority",
                "description": (
                    "Smoking is the #1 preventable cause of death. Quitting benefits emerge FAST:\n"
                    "• 20 min after quitting: blood pressure normalizes\n"
                    "• 1 year after: heart disease risk halved\n"
                    "• Use nicotine replacement therapy or varenicline\n"
                    "• Join a support group or use the Smoke Free app\n"
                    "• Set a quit date this week"
                ),
                "priority": "urgent",
                "agent_source": "recommendation+cardiologist"
            })

        # Hypertension
        if htn > 55:
            recommendations.append({
                "category": "medical",
                "title": "Blood Pressure Management",
                "description": (
                    "Your hypertension risk is elevated. Preventive actions:\n"
                    "• Reduce sodium: avoid processed foods, pickles, ready meals\n"
                    "• DASH diet: rich in fruits, vegetables, whole grains, low-fat dairy\n"
                    "• Monitor BP at home — keep a log\n"
                    "• Consult a physician for baseline blood work\n"
                    "• Limit alcohol strictly (max 1 drink/day)"
                ),
                "priority": "high",
                "agent_source": "recommendation+cardiologist"
            })

        # General preventive
        recommendations.append({
            "category": "medical",
            "title": "Annual Health Screening",
            "description": (
                "Regular checkups catch diseases before symptoms appear:\n"
                "• Fasting blood glucose + HbA1c (diabetes)\n"
                "• Lipid panel (cholesterol, triglycerides)\n"
                "• Blood pressure measurement\n"
                "• BMI and waist circumference\n"
                "• Kidney function tests (urea, creatinine)"
            ),
            "priority": "medium",
            "agent_source": "recommendation"
        })

        return recommendations
