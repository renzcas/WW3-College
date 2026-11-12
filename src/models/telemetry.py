# src/models/telemetry.py
import json

class TelemetryExporter:
    @staticmethod
    def to_json(world) -> str:
        """
        Export current world state report as a structured JSON string.
        """
        return json.dumps(world.get_world_report(), indent=2)

    @staticmethod
    def to_markdown(world) -> str:
        """
        Render a human-readable Markdown telemetry briefing.
        """
        report = world.get_world_report()
        telemetry = report["telemetry"]
        
        md = []
        md.append(f"### WORLD TELEMETRY BRIEFING — EPOCH {report['epoch_tick']}")
        md.append(f"- **World Stage:** `{report['world_stage']}`")
        md.append(f"- **Global Tension:** `{report['global_tension']}/100.0`")
        md.append(f"- **Active Nodes:** `{telemetry['active_nodes']}`")
        md.append("\n**Aggregated Resources:**")
        for res, val in telemetry["aggregated_resources"].items():
            md.append(f"- {res}: {val:.1f}")
            
        md.append("\n**Recent Events:**")
        if report["recent_events"]:
            for ev in report["recent_events"]:
                md.append(f"- `[{ev['category']}]` {ev['title']} (Score: {ev['escalation_score']})")
        else:
            md.append("- *No events logged yet.*")
            
        return "\n".join(md)