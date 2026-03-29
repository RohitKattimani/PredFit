"""Behavioral Insight Agent — detects patterns and trends across logs."""
from typing import List


class BehavioralInsightAgent:
    name = "Behavioral Insight"

    def analyze(self, logs: list, user_data: dict) -> dict:
        if not logs:
            return {
                "agent": self.name,
                "patterns": [],
                "habit_score": 50,
                "trends": {},
                "summary": "Not enough data to detect behavioral patterns yet. Keep logging!"
            }

        patterns = []
        trends = {}

        # Sleep trend
        sleep_vals = [l.sleep_hours for l in logs if l.sleep_hours]
        if len(sleep_vals) >= 3:
            avg_sleep = sum(sleep_vals) / len(sleep_vals)
            recent_sleep = sum(sleep_vals[:3]) / 3
            trends["sleep"] = {
                "avg": round(avg_sleep, 1),
                "recent": round(recent_sleep, 1),
                "direction": "improving" if recent_sleep > avg_sleep else "declining"
            }
            if avg_sleep < 6.5:
                patterns.append({
                    "pattern": "chronic_sleep_deficit",
                    "description": f"Averaged only {avg_sleep:.1f}h/night over {len(sleep_vals)} days. Chronic sleep debt is accumulating.",
                    "severity": "warning"
                })

        # Sugar trend
        sugar_vals = [l.sugar_intake_g for l in logs if l.sugar_intake_g]
        if len(sugar_vals) >= 3:
            avg_sugar = sum(sugar_vals) / len(sugar_vals)
            trends["sugar"] = {
                "avg": round(avg_sugar, 1),
                "direction": "high" if avg_sugar > 50 else "normal"
            }
            if avg_sugar > 60:
                patterns.append({
                    "pattern": "consistently_high_sugar",
                    "description": f"Sugar intake has averaged {avg_sugar:.0f}g/day. This sustained level strongly elevates diabetes risk.",
                    "severity": "critical"
                })

        # Stress trend
        stress_vals = [l.stress_level for l in logs if l.stress_level]
        if len(stress_vals) >= 3:
            avg_stress = sum(stress_vals) / len(stress_vals)
            trends["stress"] = {
                "avg": round(avg_stress, 1),
                "direction": "high" if avg_stress > 6 else "normal"
            }
            if avg_stress > 7:
                patterns.append({
                    "pattern": "chronic_stress",
                    "description": f"Stress levels have been at {avg_stress:.1f}/10 on average. Chronic stress is a silent disease catalyst.",
                    "severity": "warning"
                })

        # Exercise trend
        exercise_vals = [l.exercise_minutes for l in logs if l.exercise_minutes is not None]
        if len(exercise_vals) >= 3:
            active_days = sum(1 for e in exercise_vals if e >= 30)
            trends["exercise"] = {
                "avg_minutes": round(sum(exercise_vals) / len(exercise_vals), 1),
                "active_days": active_days,
                "total_days": len(exercise_vals)
            }
            if active_days < len(exercise_vals) * 0.4:
                patterns.append({
                    "pattern": "mostly_sedentary",
                    "description": f"Only {active_days}/{len(exercise_vals)} days had meaningful exercise. Aim for 5+ active days/week.",
                    "severity": "warning"
                })

        # Habit score calculation (out of 100)
        habit_score = 100
        for pattern in patterns:
            if pattern["severity"] == "critical":
                habit_score -= 25
            elif pattern["severity"] == "warning":
                habit_score -= 15
            else:
                habit_score -= 5
        habit_score = max(0, habit_score)

        summary = (
            f"Behavioral analysis of {len(logs)} days of data. "
            f"Habit score: {habit_score}/100. "
            + (f"Patterns detected: {', '.join(p['pattern'] for p in patterns)}." if patterns else "No concerning patterns detected. Keep up the good work!")
        )

        return {
            "agent": self.name,
            "patterns": patterns,
            "habit_score": habit_score,
            "trends": trends,
            "summary": summary
        }
