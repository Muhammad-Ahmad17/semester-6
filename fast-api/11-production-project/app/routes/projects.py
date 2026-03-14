from fastapi import APIRouter, HTTPException, Query
from app.dependencies import DB, CurrentUser
from app.models.project import DBProject
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: DB, user: CurrentUser):
    db_project = DBProject(**project.model_dump(), owner_id=user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return _to_response(db_project)


@router.get("/", response_model=list[ProjectResponse])
def list_my_projects(
    db: DB,
    user: CurrentUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    projects = (
        db.query(DBProject)
        .filter(DBProject.owner_id == user.id)
        .offset(skip).limit(limit).all()
    )
    return [_to_response(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: DB, user: CurrentUser):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    if project.owner_id != user.id and user.role != "admin":
        raise HTTPException(403, "Not your project")
    return _to_response(project)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, update: ProjectUpdate, db: DB, user: CurrentUser):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    if project.owner_id != user.id:
        raise HTTPException(403, "Not your project")

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return _to_response(project)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: DB, user: CurrentUser):
    project = db.query(DBProject).filter(DBProject.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    if project.owner_id != user.id and user.role != "admin":
        raise HTTPException(403, "Not your project")
    db.delete(project)
    db.commit()


def _to_response(project: DBProject) -> dict:
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "owner_id": project.owner_id,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "task_count": len(project.tasks),
    }
