from typing import List

from fastapi import APIRouter, UploadFile, File, Body, Depends, HTTPException
from models import Member, ProjectRole, Subteam, SubteamRole
from sqlmodel import Session, select
from db import get_session

router = APIRouter()


@router.get("/get_member_data/{member_id}", response_model=Member)
async def get_member(member_id: int, session: Session = Depends(get_session)):
    member = session.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.get("/overview-members", response_model=List[Member])
async def get_overview_members(session: Session = Depends(get_session)):
    members = session.exec(select(Member).where(Member.is_retired == 0)).all()
    if not members:
        raise HTTPException(status_code=404, detail="No members found")
    return members


@router.get("/filter/{discipline}/{role}/{project_id}", response_model=list[Member])
async def get_members_by_discipline_and_role_and_project_id(discipline: str, role: str, project_id: int,
                                                            session: Session = Depends(get_session)):
    # Start building the query
    query = select(Member).join(ProjectRole)

    # Add condition for discipline if it's not an empty string
    if discipline != '*':
        query = query.where(Member.discipline == discipline)

    # Add condition for role if it's not an empty string
    if role != '*':
        query = query.where(ProjectRole.name == role)

    # Add condition for project_id if it's not -1
    if project_id != -1:
        query = query.where(ProjectRole.project_id == project_id)

    # Execute the query
    results = session.exec(query).all()

    # Return the results
    if not results:
        raise HTTPException(status_code=404, detail="No members found matching the criteria")

    return results
