from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Issue:
    id: str
    title: str
    description: str
    priority: int
    created_at: datetime
    updated_at: datetime
    status: str
    tags: List[str]
    related_issues: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Issue':
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            status=data["status"],
            tags=data["tags"],
            related_issues=data["related_issues"]
        )