from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut
from app.core.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

# タスク追加
@router.post("/", response_model=TaskOut)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_task = Task(
        title = task.title,
        description = task.description,
        user_id = current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task

# タスク全件取得
@router.get("/", response_model=list[TaskOut])
def get_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.user_id==current_user.id).all()
    
    return tasks

# タスク更新
@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_task = db.query(Task).filter(Task.id==task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    db_task.title = task.title
    db_task.description = task.description
    
    db.commit()
    db.refresh(db_task)
    
    return db_task

# タスク削除
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}