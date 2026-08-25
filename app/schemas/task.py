from pydantic import BaseModel, ConfigDict

# 共通フィールド
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    
# 入力用
class TaskCreate(TaskBase):
    pass

# 出力用
class TaskOut(TaskBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)