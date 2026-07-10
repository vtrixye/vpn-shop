from uuid import UUID
from enum import Enum
from typing import Union, List, Sequence

class UsernameType(str, Enum):
    REGULAR = "user"
    TRIAL = "user"
    TEST = "test"

class ExpireType(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    THREE_MONTHS = "3MONTH"
    SIX_MONTHS = "6MONTH"
    YEAR = "YEAR"

class InternalSquad(UUID, Enum):
    TCP = UUID("dee381c9-17dd-4221-ab57-511543f58d7b")
    XHTTP = UUID("0482bba9-5c24-4f19-b3d9-74bc900cd947")
    HYSTERIA2 = UUID("e7f87a6d-f70a-4f70-ac1b-909671fb09d3")
    CDN = UUID("169aee30-d174-4510-9e2b-3a59cddc8e57")

    @classmethod
    def get_default(cls) -> List[UUID]:
        return [cls.TCP.value]

    @classmethod
    def parse_squads(cls, squads: Union['InternalSquad', Sequence['InternalSquad'], None]) -> List[UUID]:
        if squads is None:
            return cls.get_default()
        
        if isinstance(squads, InternalSquad):
            return [squads.value]
        
        if isinstance(squads, (list, tuple)):
            if not squads:
                return cls.get_default()
            return [squad.value if isinstance(squad, InternalSquad) else squad for squad in squads]
        
        raise ValueError(f"Неподдерживаемый тип для squads: {type(squads)}")