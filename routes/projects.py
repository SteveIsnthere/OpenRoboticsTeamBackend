from typing import List

from fastapi import APIRouter, UploadFile, File, Body, Depends, HTTPException
from models import Member, Project, ProjectRole, Subteam
from sqlmodel import Session, select
from db import get_session

router = APIRouter()


# @router.get("/overview-projects", response_model=List[Project])
# async def get_overview_members(session: Session = Depends(get_session)):
#     projects = session.exec(select(Project).where(Project.is_completed == 0)).all()
#     # rank the projects by the time they were created
#     projects = sorted(projects, key=lambda x: x.time, reverse=True)
#     if not projects:
#         raise HTTPException(status_code=404, detail="No projects found")
#     return projects

@router.get("/get/{newest_first}/{is_completed}", response_model=List[Project])
async def get_projects(newest_first: bool, is_completed: bool, session: Session = Depends(get_session)):
    projects = session.exec(select(Project).where(Project.is_completed == is_completed)).all()
    if newest_first:
        projects = sorted(projects, key=lambda x: x.time, reverse=True)
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    return projects


@router.post("/create")
async def create_project(project: Project, session: Session = Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return True
