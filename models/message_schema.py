from pydantic import BaseModel
from typing import Literal


class Message(BaseModel):
    sender: Literal["user","bot"]
    text:str
