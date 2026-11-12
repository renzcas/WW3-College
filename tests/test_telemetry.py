# tests/test_telemetry.py
import unittest
from models.world import World
from models.event import Event
from models.telemetry import TelemetryExporter

class TestPillar5Telemetry(unittest.TestCase):
    def test_extended_world_report(self):
        world = World()
        world.add_node("usa", {"stability": 90.0, "power": 50.0})
        world.add_node("china", {"stability": 80.0, "power": 60.0})

        event = Event(
            title="Cyber Incursion",
            description="Grid scan detected",
            category="CYBER",
            severity=40.0
        )
        world.queue_event(event)
        world.step()

        report = world.get_world_report()
        self.assertEqual(report["epoch_tick"], 1)
        self.assertIn("telemetry", report)
        self.assertEqual(report["telemetry"]["active_nodes"], 2)
        self.assertIn("stability", report["telemetry"]["aggregated_resources"])

    def test_telemetry_exporters(self):
        world = World()
        world.add_node("russia", {"stability": 75.0})
        
        json_out = TelemetryExporter.to_json(world)
        self.assertIsInstance(json_out, str)
        self.assertIn("epoch_tick", json_out)

        md_out = TelemetryExporter.to_markdown(world)
        self.assertIsInstance(md_out, str)
        self.assertIn("WORLD TELEMETRY BRIEFING", md_out)

if __name__ == "__main__":
    unittest.main()