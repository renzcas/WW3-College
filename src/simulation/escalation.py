# src/simulation/escalation.py
"""
Pillar 6: Simulation Escalation Module

Propagates global tension and dynamic event escalation pressures across connected nodes.
"""

def apply_escalation(world):
    """
    Adjust global tension and node stability based on active flows and tension thresholds.
    """
    if world.global_tension > 0:
        world.global_tension = max(0.0, world.global_tension - 0.5)
        world.update_world_stage()