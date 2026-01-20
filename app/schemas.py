from pydantic import BaseModel

# Used when user sends data
class ItemCreate(BaseModel):
    name: str

# Used when API returns data
class ItemResponse(ItemCreate):
    id: int

    class Config:
        # Allows SQLAlchemy object → JSON conversion
        from_attributes = True
