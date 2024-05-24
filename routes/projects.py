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
