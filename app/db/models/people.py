from typing import Optional
from db.models.common import TimestampModel, UUIDModel


class People(TimestampModel, UUIDModel, table=True):
    __tablename__ = "people"

    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    vip_score: int
    is_vip: bool

    def __repr__(self):
        return f"<Person (id: {self.id})>"
