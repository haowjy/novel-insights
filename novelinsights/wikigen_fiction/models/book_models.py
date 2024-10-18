from pydantic import BaseModel, Field
from typing import Literal, Optional

class BookModel(BaseModel):
    title: str = Field(..., description='The title of the book')