# event.py
"""
WW3-College Event Model

Core event object used throughout the simulation.

Responsibilities:
- Store normalized event information
- Calculate escalation impact
- Serialize/deserialize to JSON
- Provide validation
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any
import uuid


@dataclass
class Event:
    """
    Represents a world event entering the simulation.
    """

    title: str
    description: str
    category: str

    countries: List[str] = field(default_factory=list)
    factions: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    severity: float = 0.0
    confidence: float = 1.0
    source_reliability: float = 1.0

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    metadata: Dict[str, Any] = field(default_factory=dict)

    def escalation_score(self) -> float:
        """
        Calculate weighted escalation score.

        Formula:
            severity × confidence × reliability
        """

        return round(
            self.severity
            * self.confidence
            * self.source_reliability,
         