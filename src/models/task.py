from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Task:
    id: str
    name: str
    description: str
    priority: int
    estimated_hours: float
    assigned_to: str
    dependencies: List[str]
    phase: str
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            priority=data["priority"],
            estimated_hours=data["estimated_hours"],
            assigned_to=data["assigned_to"],
            dependencies=data["dependencies"],
            phase=data["phase"],
            status=data["status"],
            start_date=datetime.fromisoformat(data["start_date"]) if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]) if data.get("end_date") else None
        )