from pydantic import BaseModel, ConfigDict

#入力用
class UserSignup(BaseModel):
    email: str
    password: str

#出力用
class UserOut(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)