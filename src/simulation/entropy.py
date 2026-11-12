# src/simulation/entropy.py
"""
Pillar 6: Simulation Entropy Module

Applies resource decay, natural drift, and system wear across nodes per epoch tick.
"""

def apply_entropy(world, decay_rate: float = 0.01):
    """
    Apply natural resource decay (entropy) to all node states per simulation step.
    """
    for node_id, data in world.nodes.items():
        state = data.get("state", {})
        for res, val in list(state.items()):
            decayed = val * (1.0 - decay_rate)
            state[res] = max(0.0, round(decayed, 4))