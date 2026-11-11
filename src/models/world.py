# src/models/world.py
from models.snapshot import SnapshotManager

class World:
    def __init__(self):
        self.tick_count = 0
        self.nodes = {}
        self.flows = []

    def add_node(self, node_id: str, state: dict):
        self.nodes[node_id] = {"state": state}

    def add_flow(self, source: str, target: str, resource: str, rate: float):
        self.flows.append({
            "source": source,
            "target": target,
            "resource": resource,
            "rate": rate
        })

    def get_state_snapshot(self):
        return {
            "tick_count": self.tick_count,
            "nodes": self.nodes,
            "flows": self.flows
        }

    def step(self):
        # 1. Take snapshot before executing tick
        snapshot = SnapshotManager.create_snapshot(self.get_state_snapshot())

        try:
            # 2. Delta buffer for atomic updates
            deltas = {node_id: {} for node_id in self.nodes}

            # 3. Collect flow rates & enforce referential integrity
            for flow in self.flows:
                src, tgt = flow["source"], flow["target"]
                res, rate = flow["resource"], flow["rate"]
                
                if src not in self.nodes:
                    raise KeyError(f"Source node '{src}' does not exist.")
                if tgt not in self.nodes:
                    raise KeyError(f"Target node '{tgt}' does not exist.")

                deltas[src][res] = deltas[src].get(res, 0.0) - rate
                deltas[tgt][res] = deltas[tgt].get(res, 0.0) + rate

            # 4. Apply changes atomically
            for node_id, changes in deltas.items():
                for res, delta in changes.items():
                    current = self.nodes[node_id]["state"].get(res, 0.0)
                    self.nodes[node_id]["state"][res] = max(0.0, current + delta)

            self.tick_count += 1

        except Exception as e:
            # 5. Rollback on failure
            SnapshotManager.rollback(self, snapshot)
            raise