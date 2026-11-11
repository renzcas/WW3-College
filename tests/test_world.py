# tests/test_world.py
import unittest
from models.world import World

class TestWorld(unittest.TestCase):
    def test_atomic_resource_flow(self):
        world = World()
        world.add_node("usa", {"food": 100.0})
        world.add_node("japan", {"food": 50.0})
        world.add_flow("usa", "japan", "food", 10.0)

        world.step()

        self.assertEqual(world.nodes["usa"]["state"]["food"], 90.0)
        self.assertEqual(world.nodes["japan"]["state"]["food"], 60.0)
        self.assertEqual(world.tick_count, 1)

    def test_rollback_on_failure(self):
        world = World()
        world.add_node("usa", {"food": 100.0})
        
        # Introduce a malformed flow that causes a KeyError
        world.flows.append({
            "source": "usa",
            "target": "non_existent_country",
            "resource": "food",
            "rate": 10.0
        })

        initial_food = world.nodes["usa"]["state"]["food"]

        with self.assertRaises(KeyError):
            world.step()

        # Verify state rolled back cleanly
        self.assertEqual(world.nodes["usa"]["state"]["food"], initial_food)
        self.assertEqual(world.tick_count, 0)

if __name__ == "__main__":
    unittest.main()