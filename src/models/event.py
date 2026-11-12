"""
WW3-College Event Model

Core event object used throughout the simulation.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, UTC
from typing import List, Dict, Any
import uuid


@dataclass
class Event:
    """
    Represents a world event entering the simulation.
    """

    title: str
    description: str
    category: str = "GENERAL"

    countries: List[str] = field(default_factory=list)
    factions: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    severity: float = 0.0
    confidence: float = 100.0
    source_reliability: float = 100.0

    timestamp: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    metadata: Dict[str, Any] = field(default_factory=dict)

    def escalation_score(self) -> float:
        """
        Calculate weighted escalation score normalized to 0-100 scale.
        Formula:
        severity × (confidence / 100) × (reliability / 100)
        """
        return round(
            self.severity
            * (self.confidence / 100.0)
            * (self.source_reliability / 100.0),
            2
        )

    def validate(self) -> bool:
        """
        Validate required fields and ranges.
        """

        if not self.title:
            return False

        if not self.category:
            return False

        if not (0 <= self.severity <= 100):
            return False

        if not (0 <= self.confidence <= 100):
            return False

        if not (0 <= self.source_reliability <= 100):
            return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Event to serializable dict.
        """
        data = asdict(self)
        data["escalation_score"] = self.escalation_score()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Build Event from dictionary.
        """
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            category=data.get("category", "GENERAL"),
            countries=data.get("countries", []),
            factions=data.get("factions", []),
            tags=data.get("tags", []),
            severity=data.get("severity", 0.0),
            confidence=data.get("confidence", 100.0),
            source_reliability=data.get(
                "source_reliability",
                100.0
            ),
            timestamp=data.get(
                "timestamp",
                datetime.now(UTC).isoformat()
            ),
            event_id=data.get(
                "event_id",
                str(uuid.uuid4())
            ),
            metadata=data.get("metadata", {})
        )

    def summary(self) -> str:
        """
        Human readable summary.
        """
        return (
            f"[{self.category}] "
            f"{self.title} "
            f"(Score={self.escalation_score()})"
        )

    def __str__(self):
        return self.summary()


EVENT_CATEGORIES = [
    "GENERAL",
    "MILITARY",
    "CYBER",
    "ECONOMIC",
    "POLITICAL",
    "INTELLIGENCE",
    "INFORMATION",
    "TERRORISM",
    "DIPLOMACY",
    "SPACE",
    "ENERGY",
    "BIOLOGICAL",
    "CIVIL_UNREST",
]