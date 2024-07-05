from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(max_length=40)

class CategoryInfo(CategoryBase):
    id: int

    class ConfigDict:
        orm_mode = True