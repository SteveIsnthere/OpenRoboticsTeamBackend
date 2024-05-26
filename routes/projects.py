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

@router.get("/get/{is_completed}", response_model=List[Project])
async def get_projects(is_completed: bool, session: Session = Depends(get_session)):
    projects = session.exec(select(Project).where(Project.is_completed == is_completed).limit(100)).all()
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    return projects


@router.get("/get_projects_member_joined/{member_id}", response_model=List[Project])
async def get_projects_member_joined(member_id: int, session: Session = Depends(get_session)):
    projects = session.exec(select(Project).join(ProjectRole).where(ProjectRole.member_id == member_id)).all()
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    return projects


@router.get("/get_members_of_project/{project_id}", response_model=List[Member])
async def get_members_of_project(project_id: int, session: Session = Depends(get_session)):
    members = session.exec(select(Member).join(ProjectRole).where(ProjectRole.project_id == project_id)).all()
    if not members:
        raise HTTPException(status_code=404, detail="No members found")
    return members
