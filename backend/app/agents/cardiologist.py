"""Cardiologist Agent — analyzes cardiovascular indicators."""


class CardiologistAgent:
    name = "Cardiologist"

    def analyze(self, data: dict) -> dict:
        hr = data.get("heart_rate", 72)
        bp_sys = data.get("bp_systolic", 120)
        bp_dia = data.get("bp_diastolic", 80)
        exercise = data.get("exercise_minutes", 30)
        smoking = data.get("smoking", 0)
        stress = data.get("stress_level", 5)
        age = data.get("age", 35)
        bmi = data.get("bmi", 22)

        insights = []
        flags = []

        # Heart rate check
        if hr > 100:
            flags.append("tachycardia")
            insights.append({
                "type": "alert",
                "title": "Elevated Heart Rate",
                "content": f"Your resting heart rate of {hr} bpm is above normal (60-100 bpm). This could indicate stress, dehydration, or a cardiovascular concern.",
                "severity": "warning"
            })
        elif hr < 50:
            insights.append({
                "type": "alert",
                "title": "Low Resting Heart Rate",
                "content": f"Heart rate of {hr} bpm is low. This may be normal for athletes but worth monitoring.",
                "severity": "info"
            })

        # Blood pressure
        if bp_sys >= 140 or bp_dia >= 90:
            flags.append("stage2_hypertension")
            insights.append({
                "type": "risk",
                "title": "Stage 2 Hypertension Detected",
                "content": f"BP {bp_sys}/{bp_dia} mmHg is in the Stage 2 Hypertension range. Recommend immediate medical consultation.",
                "severity": "critical"
            })
        elif bp_sys >= 130 or bp_dia >= 80:
            flags.append("stage1_hypertension")
            insights.append({
                "type": "risk",
                "title": "Elevated Blood Pressure",
                "content": f"BP {bp_sys}/{bp_dia} mmHg is elevated. Consider reducing sodium intake and increasing aerobic exercise.",
                "severity": "warning"
            })

        # Exercise
        if exercise < 20:
            insights.append({
                "type": "recommendation",
                "title": "Insufficient Cardiovascular Exercise",
                "content": "You're getting less than 20 minutes of exercise. Aim for at least 150 minutes/week of moderate cardio to maintain heart health.",
                "severity": "warning"
            })

        # Smoking
        if smoking > 0:
            insights.append({
                "type": "risk",
                "title": "Smoking Risk",
                "content": f"Smoking {smoking} cigarettes daily significantly elevates CVD risk. Quitting reduces heart attack risk by 50% within 1 year.",
                "severity": "critical" if smoking > 10 else "warning"
            })

        # Summary
        risk_score = min(100, max(0,
            (max(0, bp_sys - 110) * 0.7) +
            (max(0, hr - 70) * 0.5) +
            (smoking * 2.5) +
            (stress * 2) +
            (max(0, age - 40) * 0.8) +
            (bmi * 0.4)
        ))

        summary = (
            f"Cardio risk assessed at {risk_score:.0f}/100. "
            + (f"Flags: {', '.join(flags)}. " if flags else "Cardiovascular profile looks stable. ")
            + ("Recommend reducing CV risk factors: exercise more, quit smoking." if flags else "Keep maintaining your exercise routine.")
        )

        return {
            "agent": self.name,
            "risk_score": round(risk_score, 1),
            "flags": flags,
            "insights": insights,
            "summary": summary
        }
