"""Consensus Agent — aggregates all doctor agents and produces final recommendations."""


class ConsensusAgent:
    name = "Consensus"

    def aggregate(self, user_data: dict, agent_results: dict) -> dict:
        all_flags = []
        all_insights = []
        agent_scores = []
        critical_count = 0

        for agent_name, result in agent_results.items():
            all_flags.extend(result.get("flags", []))
            for insight in result.get("insights", []):
                insight["agent"] = agent_name
                all_insights.append(insight)
                if insight.get("severity") == "critical":
                    critical_count += 1
            score = result.get("risk_score", 0)
            agent_scores.append(score)

        avg_risk = sum(agent_scores) / len(agent_scores) if agent_scores else 0
        top_risk_agent = max(agent_results.items(), key=lambda x: x[1].get("risk_score", 0))

        # Build prioritized recommendations
        top_flags = list(set(all_flags))[:5]
        key_factors = ", ".join(top_flags) if top_flags else "No major concerns detected"

        # Consensus narrative
        if avg_risk >= 70:
            urgency = "URGENT: Multiple high-risk indicators detected."
            action = "We strongly recommend consulting a physician within 48 hours."
        elif avg_risk >= 45:
            urgency = "MODERATE RISK: Several lifestyle risk factors identified."
            action = "Begin lifestyle modifications immediately and schedule a checkup."
        elif avg_risk >= 25:
            urgency = "MILD RISK: Some areas need attention."
            action = "Small consistent changes to diet, exercise, and sleep will significantly reduce your risk."
        else:
            urgency = "LOW RISK: Your health indicators look good overall."
            action = "Keep maintaining your current healthy habits."

        # Highest priority insight
        critical_insights = [i for i in all_insights if i.get("severity") == "critical"]
        warning_insights = [i for i in all_insights if i.get("severity") == "warning"]
        prioritized = critical_insights + warning_insights

        top_concern = ""
        if prioritized:
            top = prioritized[0]
            top_concern = f"Top concern from {top.get('agent', 'AI')}: {top.get('title', '')} — {top.get('content', '')[:120]}..."

        summary = (
            f"{urgency} {action} "
            f"Highest risk area: {top_risk_agent[0].replace('_', ' ').title()} "
            f"({top_risk_agent[1].get('risk_score', 0):.0f}/100). "
            f"Key factors: {key_factors}."
        )

        return {
            "agent": self.name,
            "avg_agent_risk": round(avg_risk, 1),
            "critical_count": critical_count,
            "all_flags": top_flags,
            "key_factors": key_factors,
            "top_risk_agent": top_risk_agent[0],
            "top_concern": top_concern,
            "urgency_level": "urgent" if avg_risk >= 70 else "moderate" if avg_risk >= 45 else "mild" if avg_risk >= 25 else "low",
            "all_insights": all_insights,
            "summary": summary
        }
