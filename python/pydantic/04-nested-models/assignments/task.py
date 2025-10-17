from pydantic import BaseModel #type: ignore
from typing import List

# TODO: Create Course model
# Each Course has modules
# Each Module has lessons



class Lesson(BaseModel):
    id: int
    topic: str
class Module(BaseModel):
    id: int
    name: str
    lessons: List[Lesson]
class Course(BaseModel):
    id: int
    title: str
    modules: List[Module]