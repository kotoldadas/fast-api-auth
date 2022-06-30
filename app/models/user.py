from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserLogin(SQLModel):
    username: str
    password: str
