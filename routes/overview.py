from typing import List

from fastapi import APIRouter, UploadFile, File, Body, Depends, HTTPException
from models import Member, Project, ProjectRole, Subteam, SubteamRole
from sqlmodel import Session, select
from db import get_session

router = APIRouter()


@router.get("/data")
async def get_overview_data(session: Session = Depends(get_session)):
    async def get_overview_members(session: Session = Depends(get_session)):
        members = session.exec(select(Member).where(Member.is_retired == 0)).all()
        if not members:
            raise HTTPException(status_code=404, detail="No members found")
        return members

    async def get_overview_projects(session: Session = Depends(get_session)):
        projects = session.exec(select(Project).where(Project.is_completed == 0)).all()
        # rank the projects by the time they were created
        projects = sorted(projects, key=lambda x: x.time, reverse=True)
        if not projects:
            raise HTTPException(status_code=404, detail="No projects found")
        return projects

    async def get_overview_roles(project_ids: List[int], session: Session = Depends(get_session)):
        roles = session.exec(select(ProjectRole)).all()
        roles = [role for role in roles if role.project_id in project_ids]
        if not roles:
            raise HTTPException(status_code=404, detail="No roles found")
        return roles

    async def get_overview_subteams(project_ids: List[int], session: Session = Depends(get_session)):
        subteams = session.exec(select(Subteam)).all()
        subteams = [subteam for subteam in subteams if subteam.project_id in project_ids]
        if not subteams:
            raise HTTPException(status_code=404, detail="No subteams found")
        return subteams

    async def get_overview_subteam_roles(subteams_ids: List[int], session: Session = Depends(get_session)):
        subteam_roles = session.exec(select(SubteamRole)).all()
        subteam_roles = [subteam_role for subteam_role in subteam_roles if subteam_role.subteam_id in subteams_ids]
        if not subteam_roles:
            raise HTTPException(status_code=404, detail="No subteam roles found")
        return subteam_roles

    members = await get_overview_members(session)
    projects = await get_overview_projects(session)

    project_ids = [project.id for project in projects]
    roles = await get_overview_roles(project_ids, session=session)
    subteams = await get_overview_subteams(project_ids, session=session)

    subteam_ids = [subteam.id for subteam in subteams]
    subteam_roles = await get_overview_subteam_roles(subteam_ids, session=session)
    return {"projects": projects, "roles": roles, "subteams": subteams, "members": members,
            "subteam_roles": subteam_roles}
