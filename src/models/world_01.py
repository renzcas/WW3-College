import copy

from models.snapshot import SnapshotManager


class World:

    def __init__(self):
        self.tick_count = 0
        self.nodes = {}
        self.flows = []

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
        Validate and queue an incoming event.
        """

        if not event.validate():
            raise ValueError(
                "Invalid event parameters."
            )

        self.event_queue.append(event)

    def process_events(self):
        """
        Drain event queue and update
        world tension/state.
        """

        while self.event_queue:

            event = self.event_queue.pop(0)

            self.event_history.append(event)

            self.global_tension += (
                event.escalation_score()
            )

            self.global_tension = min(
                self.global_tension,
                100.0
            )

        self.update_world_stage()

    def update_world_stage(self):

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
        Produce a reporting snapshot.
        """

        aggregated_resources = {}

        for node in self.nodes.values():

            for resource, value in node["state"].items():

                aggregated_resources[resource] = (
                    aggregated_resources.get(
                        resource,
                        0.0
                    )
                    + value
                )

        recent_events = [
            {
                "title": e.title,
                "category": e.category,
                "escalation_score": (
                    e.escalation_score()
                )
            }
            for e in self.event_history[-5:]
        ]

        return {

            "epoch_tick":
                self.tick_count,

            "world_stage":
                self.world_stage,

            "global_tension":
                round(
                    self.global_tension,
                    2
                ),

            "recent_events":
                recent_events,

            "telemetry": {

                "active_nodes":
                    len(self.nodes),

                "aggregated_resources":
                    aggregated_resources
            }
        }

    def get_state_snapshot(self):

        return copy.deepcopy({

            "tick_count":
                self.tick_count,

            "nodes":
                self.nodes,

            "flows":
                self.flows,

            "event_queue":
                self.event_queue,

            "event_history":
                self.event_history,

            "global_tension":
                self.global_tension,

            "world_stage":
                self.world_stage
        })

    def step(self):

        snapshot = SnapshotManager.create_snapshot(
            self.get_state_snapshot()
        )

        try:

            self.process_events()

            deltas = {
                node_id: {}
                for node_id in self.nodes
            }

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
                    deltas[src].get(
                        res,
                        0.0
                    ) - rate
                )

                deltas[tgt][res] = (
                    deltas[tgt].get(
                        res,
                        0.0
                    ) + rate
                )

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

            SnapshotManager.rollback(
                self,
                snapshot
            )

            raise