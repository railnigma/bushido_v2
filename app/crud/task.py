from sqlalchemy.orm import Session

from app.db.models import Task
from app.schemas.task import TaskCreate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        task_date=task_data.task_date,
        status=task_data.status.value,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()