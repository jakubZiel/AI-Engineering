from pydantic import BaseModel


class Purchase(BaseModel):
    company : int
    user_id : int
    city : int
