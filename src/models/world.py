# src/models/world.py

import copy

from models.snapshot import SnapshotManager


class World:

    def __init__(self):
        self.tick_count = 0
        self.nodes = {}
        self.flows = []
        
        # Pillar 3 & 4 Native Event & Tension Engine State
        self.event_queue = []
        self.event_history = []
        self.global_tension = 0.0
        self.world_stage = "PEACE"

    def add_node(self, node_id: str, state: dict):

        self.nodes[node_id] = {
            "state": state
        }

    def add_flow(
        self,
        source: str,
        target: str,
        resource: str,
        rate: float
    ):

        if rate < 0:
            raise ValueError(
                "Flow rate cannot be negative."
            )

        self.flows.append({
            "source": source,
            "target": target,
            "resource": resource,
            "rate": rate
        })

    def queue_event(self, event):
        """
        Validate and queue an incoming event for simulation processing.
        """
        if not event.validate():
            raise ValueError("Invalid event parameters or out-of-range metrics.")
        self.event_queue.append(event)

    def process_events(self):
        """
        Drain the event queue, push to history, and mutate global tension/stages.
        """
        while self.event_queue:
            event = self.event_queue.pop(0)
            self.event_history.append(event)
            
            # Accumulate tension based on normalized escalation score
            self.global_tension += event.escalation_score()
            self.global_tension = min(self.global_tension, 100.0)
            
            self.update_world_stage()

    def update_world_stage(self):
        """
        Determine current geopolitical stage based on global tension thresholds.
        """
        t = self.global_tension
        if t < 20:
            self.world_stage = "PEACE"
        elif t < 40:
            self.world_stage = "COMPETITION"
        elif t < 60:
            self.world_stage = "CRISIS"
        elif t < 80:
            self.world_stage = "REGIONAL_WAR"
        else:
            self.world_stage = "GLOBAL_WAR_RISK"

    def get_world_report(self) -> dict:
        """
        Generate a summary snapshot of the current simulation epoch.
        """
        recent_events = [e.title for e in self.event_history[-5:]]
        return {
            "tick": self.tick_count,
            "world_stage": self.world_stage,
            "global_tension": round(self.global_tension, 2),
            "recent_events": recent_events,
            "nodes_count": len(self.nodes)
        }

    def get_state_snapshot(self):

        return copy.deepcopy({
            "tick_count": self.tick_count,
            "nodes": self.nodes,
            "flows": self.flows,
            "event_queue": self.event_queue,
            "event_history": self.event_history,
            "global_tension": self.global_tension,
            "world_stage": self.world_stage
        })

    def step(self):

        # 1. Take snapshot before executing tick
        snapshot = SnapshotManager.create_snapshot(
            self.get_state_snapshot()
        )

        try:
            # 2. Process queued events before physics flows execute
            self.process_events()

            # 3. Delta buffer for atomic updates
            deltas = {
                node_id: {}
                for node_id in self.nodes
            }

            # 4. Collect flow rates &
            #    enforce referential integrity
            for flow in self.flows:

                src = flow["source"]
                tgt = flow["target"]
                res = flow["resource"]
                rate = flow["rate"]

                if src not in self.nodes:
                    raise KeyError(
                        f"Source node '{src}' does not exist."
                    )

                if tgt not in self.nodes:
                    raise KeyError(
                        f"Target node '{tgt}' does not exist."
                    )

                deltas[src][res] = (
                    deltas[src].get(res, 0.0) - rate
                )

                deltas[tgt][res] = (
                    deltas[tgt].get(res, 0.0) + rate
                )

            # 5. Apply changes atomically
            for node_id, changes in deltas.items():

                for res, delta in changes.items():

                    current = (
                        self.nodes[node_id]["state"]
                        .get(res, 0.0)
                    )

                    self.nodes[node_id]["state"][res] = max(
                        0.0,
                        current + delta
                    )

            self.tick_count += 1

        except Exception:

            # 6. Rollback on failure
            SnapshotManager.rollback(
                self,
                snapshot
            )

            raise