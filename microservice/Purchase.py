from pydantic import BaseModel
from typing import List

class Purchase(BaseModel):
    city : int
    street : int
    product_name : int
    category_path : int
    price : int
    delivery_company : int
    week_day : int
    purchase_week_day_plus_hour : int
    
    def toVector(self) -> list:
        return [
            self.city,
            self.street,
            self.product_name,
            self.category_path,
            self.price,
            self.delivery_company,
            self.week_day,
            self.purchase_week_day_plus_hour
        ]
    