from pydantic import BaseModel

class GachaResult(BaseModel):
    name: str
    tier_level: int
    tier_name: str
    chance: float
