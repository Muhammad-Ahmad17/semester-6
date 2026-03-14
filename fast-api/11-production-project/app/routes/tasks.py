from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.dependencies import DB, CurrentUser
from app.models.task import DBTask, TaskStatus, TaskPriority
from app.models.project import DBProject
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(project_id: int, task: TaskCreate, db: DB, user: CurrentUser):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    if project.owner_id != user.id and user.role != "admin":
        raise HTTPException(403, "Not your project")

    db_task = DBTask(**task.model_dump(), project_id=project_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    project_id: int,
    db: DB,
    user: CurrentUser,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee_id: Optional[int] = None,
):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    query = db.query(DBTask).filter(DBTask.project_id == project_id)
    if status:
        query = query.filter(DBTask.status == status.value)
    if priority:
        query = query.filter(DBTask.priority == priority.value)
    if assignee_id:
        query = query.filter(DBTask.assignee_id == assignee_id)

    return query.all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(project_id: int, task_id: int, db: DB, user: CurrentUser):
    task = db.query(DBTask).filter(DBTask.id == task_id, DBTask.project_id == project_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(project_id: int, task_id: int, update: TaskUpdate, db: DB, user: CurrentUser):
    task = db.query(DBTask).filter(DBTask.id == task_id, DBTask.project_id == project_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    for key, value in update.model_dump(exclude_unset=True).items():
        if isinstance(value, (TaskStatus, TaskPriority)):
            value = value.value
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(project_id: int, task_id: int, db: DB, user: CurrentUser):
    task = db.query(DBTask).filter(DBTask.id == task_id, DBTask.project_id == project_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    db.delete(task)
    db.commit()
