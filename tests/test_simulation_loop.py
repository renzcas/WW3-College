# tests/test_simulation_loop.py
import unittest
from models.world import World
from models.event import Event

class TestSimulationLoop(unittest.TestCase):
    def test_entropy_decay_per_tick(self):
        world = World()
        world.add_node("usa", {"food": 100.0})
        
        initial_food = world.nodes["usa"]["state"]["food"]
        world.step()
        
        current_food = world.nodes["usa"]["state"]["food"]
        self.assertLess(current_food, initial_food)

    def test_escalation_decay_and_heartbeat(self):
        world = World()
        world.global_tension = 50.0
        world.update_world_stage()
        
        world.step()
        
        self.assertLess(world.global_tension, 50.0)

if __name__ == "__main__":
    unittest.main()