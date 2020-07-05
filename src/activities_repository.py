from dataclasses import dataclass
from typing import Optional


@dataclass
class FindActivitiesCriteria:
    category: Optional[str] = None
    location: Optional[str] = None
    district: Optional[str] = None
    from_time: Optional[str] = None
    to_time: Optional[str] = None
