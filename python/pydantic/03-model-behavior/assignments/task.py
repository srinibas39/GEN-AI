from pydantic import BaseModel, Field , computed_field

# TODO: Create Booking model
# Fields:
# - user_id: int
# - room_id: int
# - nights: int (must be >=1)
# - rate_per_night: float
# Also, add computed field: total_amount = nights * rate_per_night

class BookingModel(BaseModel):
    user_id: int
    root_id: int
    nights: int = Field(...,ge = 1)
    rate_per_night:float
    
    @computed_field
    @property
    def total_amount(self) -> float:
        return self.nights * self.rate_per_night


