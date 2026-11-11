# src/models/world.py

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

    def step(self):
        # 1. Delta buffer for atomic updates
        deltas = {node_id: {} for node_id in self.nodes}

        # 2. Collect flow rates
        for flow in self.flows:
            src, tgt = flow["source"], flow["target"]
            res, rate = flow["resource"], flow["rate"]
            
            if src in self.nodes and tgt in self.nodes:
                deltas[src][res] = deltas[src].get(res, 0.0) - rate
                deltas[tgt][res] = deltas[tgt].get(res, 0.0) + rate

        # 3. Apply changes atomically
        for node_id, changes in deltas.items():
            for res, delta in changes.items():
                current = self.nodes[node_id]["state"].get(res, 0.0)
                self.nodes[node_id]["state"][res] = max(0.0, current + delta)

        self.tick_count += 1