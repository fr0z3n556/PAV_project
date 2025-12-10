from pydantic import BaseModel
from typing import Optional

class MessageSchema(BaseModel):
    """
    Схема для валидации сообщений об успешном выполнении операций.
    
    Параметры:
    message (str): Сообщение об успешном выполнении операции.
    """
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Операция выполнена успешно"
            }
        }