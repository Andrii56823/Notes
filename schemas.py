from pydantic import BaseModel, Field

class Note(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    content: str = Field(min_length=2, max_length=50)


class NoteOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=2, max_length=50)

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str