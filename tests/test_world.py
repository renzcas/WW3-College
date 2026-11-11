import unittest

from models.world import World


class TestWorld(unittest.TestCase):

    def test_atomic_resource_flow(self):

        world = World()

        world.add_node(
            "usa",
            {"food": 100.0}
        )

        world.add_node(
            "japan",
            {"food": 50.0}
        )

        world.add_flow(
            "usa",
            "japan",
            "food",
            10.0
        )

        world.step()

        self.assertEqual(
            world.nodes["usa"]["state"]["food"],
            90.0
        )

        self.assertEqual(
            world.nodes["japan"]["state"]["food"],
            60.0
        )

        self.assertEqual(
            world.tick_count,
            1
        )

    def test_rollback_on_failure(self):

        world = World()

        world.add_node(
            "usa",
            {"food": 100.0}
        )

        world.add_flow(
            "usa",
            "non_existent_country",
            "food",
            10.0
        )

        with self.assertRaises(KeyError):
            world.step()

        self.assertEqual(
            world.tick_count,
            0
        )

        self.assertEqual(
            world.nodes["usa"]["state"]["food"],
            100.0
        )

    def test_multiple_flow_atomicity(self):

        world = World()

        world.add_node(
            "usa",
            {"food": 100.0}
        )

        world.add_node(
            "japan",
            {"food": 0.0}
        )

        world.add_node(
            "korea",
            {"food": 0.0}
        )

        world.add_flow(
            "usa",
            "japan",
            "food",
            10.0
        )

        world.add_flow(
            "usa",
            "korea",
            "food",
            20.0
        )

        world.step()

        self.assertEqual(
            world.nodes["usa"]["state"]["food"],
            70.0
        )

        self.assertEqual(
            world.nodes["japan"]["state"]["food"],
            10.0
        )

        self.assertEqual(
            world.nodes["korea"]["state"]["food"],
            20.0
        )

    def test_snapshot_isolation(self):

        world = World()

        world.add_node(
            "usa",
            {"food": 100.0}
        )

        snapshot = world.get_state_snapshot()

        world.nodes["usa"]["state"]["food"] = 999.0

        self.assertEqual(
            snapshot["nodes"]["usa"]["state"]["food"],
            100.0
        )

    def test_negative_resource_rate(self):

        world = World()

        world.add_node(
            "usa",
            {"food": 100.0}
        )

        world.add_node(
            "japan",
            {"food": 50.0}
        )

        with self.assertRaises(ValueError):

            world.add_flow(
                "usa",
                "japan",
                "food",
                -10.0
            )


if __name__ == "__main__":
    unittest.main()