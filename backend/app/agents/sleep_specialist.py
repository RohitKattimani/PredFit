"""Sleep Specialist Agent — analyzes sleep quality and patterns."""


class SleepSpecialistAgent:
    name = "Sleep Specialist"

    def analyze(self, data: dict) -> dict:
        sleep_hours = data.get("sleep_hours", 7)
        sleep_quality = data.get("sleep_quality", 5)
        stress = data.get("stress_level", 5)
        bmi = data.get("bmi", 22)
        age = data.get("age", 35)

        insights = []
        flags = []

        # Sleep duration
        if sleep_hours < 5:
            flags.append("severe_sleep_deprivation")
            insights.append({
                "type": "alert",
                "title": "Severe Sleep Deprivation",
                "content": f"Only {sleep_hours}h of sleep! Below 5h severely raises risk of heart disease, diabetes, obesity, and immune dysfunction. Aim for 7-9 hours.",
                "severity": "critical"
            })
        elif sleep_hours < 6.5:
            flags.append("sleep_deprived")
            insights.append({
                "type": "warning",
                "title": "Insufficient Sleep",
                "content": f"{sleep_hours}h of sleep is below the recommended 7-9h for adults. Chronic sleep debt impairs cognition and metabolism.",
                "severity": "warning"
            })
        elif sleep_hours > 9.5:
            insights.append({
                "type": "info",
                "title": "Excessive Sleep",
                "content": f"{sleep_hours}h of sleep may indicate fatigue, depression, or sleep apnea. Consistently over 9h is associated with increased mortality risk.",
                "severity": "info"
            })

        # Sleep quality
        if sleep_quality <= 3:
            flags.append("poor_sleep_quality")
            insights.append({
                "type": "warning",
                "title": "Poor Sleep Quality",
                "content": "Low sleep quality indicates poor restorative sleep. This could be caused by stress, screen time, caffeine, or sleep apnea. Try a consistent bedtime and limit screens 1h before sleep.",
                "severity": "warning"
            })
        elif sleep_quality <= 5:
            insights.append({
                "type": "recommendation",
                "title": "Suboptimal Sleep Quality",
                "content": "Sleep quality can be improved. Ensure your bedroom is cool (18-20°C), dark, and avoid caffeine after 2pm.",
                "severity": "info"
            })

        # Obesity + Sleep apnea risk
        if bmi > 30 and sleep_quality < 6:
            flags.append("sleep_apnea_risk")
            insights.append({
                "type": "risk",
                "title": "Sleep Apnea Risk",
                "content": "High BMI combined with poor sleep quality raises the risk of obstructive sleep apnea. Consider a sleep study (polysomnography).",
                "severity": "warning"
            })

        # Stress effect on sleep
        if stress > 7 and sleep_hours < 7:
            insights.append({
                "type": "info",
                "title": "Stress-Sleep Feedback Loop",
                "content": "High stress and poor sleep create a harmful cycle. Addressing stress through meditation, journaling, or therapy can break this loop.",
                "severity": "info"
            })

        risk_score = min(100, max(0,
            (max(0, 7 - sleep_hours) * 15) +
            ((10 - sleep_quality) * 5) +
            (stress * 2)
        ))

        summary = (
            f"Sleep risk calculated at {risk_score:.0f}/100. "
            + (f"Issues: {', '.join(flags)}. " if flags else "Sleep seems adequate overall. ")
            + "Target 7-9h of quality, uninterrupted sleep for optimal health."
        )

        return {
            "agent": self.name,
            "risk_score": round(risk_score, 1),
            "flags": flags,
            "insights": insights,
            "summary": summary
        }
