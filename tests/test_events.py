import unittest

from models.world import World
from models.event import Event


class TestEvents(unittest.TestCase):

    def test_queue_event(self):

        world = World()

        event = Event(
            title="Cyber Attack",
            description="Infrastructure disruption",
            category="CYBER",
            severity=50,
            confidence=100,
            source_reliability=100
        )

        world.queue_event(event)

        self.assertEqual(
            len(world.event_queue),
            1
        )

    def test_process_event(self):

        world = World()

        event = Event(
            title="Market Shock",
            description="Economic turbulence",
            category="ECONOMIC",
            severity=50,
            confidence=100,
            source_reliability=100
        )

        world.queue_event(event)

        world.step()

        self.assertEqual(
            len(world.event_history),
            1
        )

        self.assertEqual(
            len(world.event_queue),
            0
        )

    def test_global_tension_increases(self):

        world = World()

        event = Event(
            title="Border Clash",
            description="Military confrontation",
            category="MILITARY",
            severity=100,
            confidence=100,
            source_reliability=100
        )

        world.queue_event(event)

        world.step()

        self.assertGreater(
            world.global_tension,
            0
        )

    def test_world_stage_transition(self):

        world = World()

        event = Event(
            title="Missile Strike",
            description="High severity incident",
            category="MILITARY",
            severity=100,
            confidence=100,
            source_reliability=100
        )

        world.queue_event(event)

        world.step()

        self.assertNotEqual(
            world.world_stage,
            "PEACE"
        )

    def test_world_report(self):

        world = World()

        world.add_node(
            "usa",
            {
                "food": 100.0,
                "energy": 50.0
            }
        )

        event = Event(
            title="Cyber Attack",
            description="Testing report",
            category="CYBER",
            severity=80,
            confidence=100,
            source_reliability=100
        )

        world.queue_event(event)

        world.step()

        report = world.get_world_report()

        self.assertIn(
            "epoch_tick",
            report
        )

        self.assertIn(
            "world_stage",
            report
        )

        self.assertIn(
            "global_tension",
            report
        )

        self.assertIn(
            "telemetry",
            report
        )

        self.assertEqual(
            report["telemetry"]["active_nodes"],
            1
        )

    def test_report_contains_recent_events(self):

        world = World()

        event = Event(
            title="Trade Embargo",
            description="Economic pressure")