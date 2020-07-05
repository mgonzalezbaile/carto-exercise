import abc
from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class FindActivitiesCriteria:
    category: Optional[str] = None
    location: Optional[str] = None
    district: Optional[str] = None
    from_time: Optional[str] = None
    to_time: Optional[str] = None


class ActivitiesRepository(ABC):
    @abc.abstractmethod
    def fetch_activities_by_criteria_geojson(self, criteria: FindActivitiesCriteria) -> dict:
        pass

    @abc.abstractmethod
    def fetch_recommended_activity_by_criteria_geojson(self, criteria: FindActivitiesCriteria) -> dict:
        pass
