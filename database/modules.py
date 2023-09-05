from typing import Optional
from sqlmodel import Field, SQLModel, Column, TEXT
from datetime import datetime


class UserPayment(SQLModel, table=True):
    __tablename__ = "user_payment"
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    chat_id: str
    payed_id: str
    paid: bool = Field(default=False)
    package_plan: str
    subscription_start_date = Field(default=datetime.now())
    subscription_expired: bool = Field(default=False)