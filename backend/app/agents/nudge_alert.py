"""Nudge & Alert Agent — checks thresholds and generates alerts/reminders."""
from datetime import datetime


class NudgeAlertAgent:
    name = "Nudge & Alert"

    def check(self, user_data: dict, risk_scores: dict) -> list:
        alerts = []
        now = datetime.now()
        hour = now.hour

        diabetes = risk_scores.get("diabetes", 0)
        hypertension = risk_scores.get("hypertension", 0)
        cvd = risk_scores.get("cvd", 0)
        overall = risk_scores.get("overall", 0)

        sleep = user_data.get("sleep_hours", 7)
        water = user_data.get("water_ml", 2000)
        steps = user_data.get("steps_count", 5000)
        stress = user_data.get("stress_level", 5)
        exercise = user_data.get("exercise_minutes", 30)
        smoking = user_data.get("smoking", 0)
        bp_sys = user_data.get("bp_systolic", 120)

        # Critical risk alerts
        if overall >= 70:
            alerts.append({
                "type": "alert",
                "severity": "critical",
                "title": "⚠️ Critical Health Risk",
                "message": f"Your overall health risk score is {overall:.0f}/100. Immediate lifestyle changes and medical consultation are strongly recommended.",
                "action": "Book a doctor appointment"
            })

        if diabetes >= 65:
            alerts.append({
                "type": "alert",
                "severity": "critical",
                "title": "🩸 High Diabetes Risk",
                "message": f"Diabetes risk at {diabetes:.0f}%. Get an HbA1c test and eliminate sugary foods.",
                "action": "Schedule HbA1c test"
            })

        if hypertension >= 60 or bp_sys >= 140:
            alerts.append({
                "type": "alert",
                "severity": "critical",
                "title": "💊 Hypertension Alert",
                "message": f"Hypertension risk is {hypertension:.0f}% with BP {bp_sys}. Reduce sodium, exercise, and see a doctor.",
                "action": "Measure blood pressure daily"
            })

        if cvd >= 60:
            alerts.append({
                "type": "alert",
                "severity": "critical",
                "title": "❤️ Cardiovascular Risk",
                "message": f"CVD risk at {cvd:.0f}%. Prioritize heart-healthy diet and aerobic exercise.",
                "action": "Schedule cardiology consultation"
            })

        # Nudge reminders
        if water < 1000:
            alerts.append({
                "type": "nudge",
                "severity": "info",
                "title": "💧 Drink More Water",
                "message": "You've had very little water today. Hydration is critical for metabolism and kidney health.",
                "action": "Drink a glass of water now"
            })

        if steps < 2000 and hour >= 14:
            alerts.append({
                "type": "nudge",
                "severity": "warning",
                "title": "🚶 Time to Move!",
                "message": "You've only taken 2,000 steps today. Take a 15-minute walk to boost your daily activity.",
                "action": "Take a walk"
            })

        if sleep < 5:
            alerts.append({
                "type": "nudge",
                "severity": "warning",
                "title": "😴 Sleep Debt Accumulating",
                "message": "Less than 5h of sleep detected. Prioritize sleep tonight — aim for 8 hours.",
                "action": "Set a 10pm bedtime alarm"
            })

        if stress >= 8:
            alerts.append({
                "type": "nudge",
                "severity": "warning",
                "title": "🧘 Take a Stress Break",
                "message": "Your stress level is very high. Take 5 minutes for deep breathing or a short walk.",
                "action": "Open breathing exercise"
            })

        if smoking > 0:
            alerts.append({
                "type": "nudge",
                "severity": "warning",
                "title": "🚭 Quit Smoking Reminder",
                "message": f"You smoked {smoking} cigarettes today. Each cigarette shortens life expectancy by 11 minutes.",
                "action": "View quitting resources"
            })

        # Evening nudges
        if hour >= 20 and exercise == 0:
            alerts.append({
                "type": "nudge",
                "severity": "info",
                "title": "🌙 No Exercise Today",
                "message": "You haven't exercised today. A quick 15-min evening walk still counts!",
                "action": "Log a walk"
            })

        return alerts
