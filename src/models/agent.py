from dataclasses import dataclass


@dataclass
class Agent:

    name: str

    escalation: float = 0.0

    influence: float = 1.0

    trust: float = 0.5

    resources: float = 100.0