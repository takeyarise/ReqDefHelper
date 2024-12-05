from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from .issue import Issue

@dataclass
class Project:
    id: str
    title: str
    description: str
    goals: List[str]
    issues: List[Issue]
    created_at: datetime
    updated_at: datetime
    status: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            goals=data["goals"],
            issues=[Issue.from_dict(issue) for issue in data["issues"]],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            status=data["status"]
        )