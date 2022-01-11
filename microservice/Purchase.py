from pydantic import BaseModel
from typing import List

class Purchase(BaseModel):
    city : int
    street : int
    purchase_week_day_plus_hour : int
    
    def toVector(self) -> list:
        return [
            self.city,
            self.street,
            self.purchase_week_day_plus_hour
        ]
    