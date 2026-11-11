# src/models/snapshot.py
import copy

class SnapshotManager:
    @staticmethod
    def create_snapshot(world_state):
        """Creates a deep copy snapshot of the world state."""
        return copy.deepcopy(world_state)

    @staticmethod
    def rollback(world, snapshot):
        """Restores the world state from a previous snapshot."""
        world.tick_count = snapshot["tick_count"]
        world.nodes = copy.deepcopy(snapshot["nodes"])
        world.flows = copy.deepcopy(snapshot["flows"])