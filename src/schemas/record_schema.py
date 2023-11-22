from pydantic import BaseModel


class Record(BaseModel):
    record_id: int
    name: str
    location: str
