from sqlmodel import SQLModel, Field
from typing import Optional

class GroupType(SQLModel, table=True):
    __tablename__ = "group_type"
    
    group_type_id: Optional[int] = Field(default=None, primary_key=True)
    group_type_name: Optional[str] = Field(max_length=20)