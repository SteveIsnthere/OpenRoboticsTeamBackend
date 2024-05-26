from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, Body, Depends, HTTPException
from pydantic import BaseModel

from models import Member
from sqlmodel import Session, select
from db import get_session
from datetime import datetime

router = APIRouter()


@router.get("/get_member_data/{member_id}", response_model=Member)
async def get_member(member_id: int, session: Session = Depends(get_session)):
    member = session.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.get("/get_retired_members", response_model=List[Member])
async def get_retired_members(session: Session = Depends(get_session)):
    members = session.exec(select(Member).where(Member.is_retired == 1).limit(100)).all()
    if not members:
        raise HTTPException(status_code=404, detail="No retired members found")
    return members


@router.post("/get_members_with_name", response_model=List[Member])
async def get_members_with_name(name: str = Body(...), session: Session = Depends(get_session)):
    # return members whose name contains the given string
    members = session.exec(select(Member).where(Member.name.contains(name)).limit(100)).all()
    if not members:
        raise HTTPException(status_code=404, detail="No members found")
    return members


# @router.put("/update_member/{member_id}")
# async def update_member(member_id: int, member: Member = Body(...), session: Session = Depends(get_session)):
#     db_member = session.get(Member, member_id)
#     if not db_member:
#         raise HTTPException(status_code=404, detail="Member not found")
#     update_data = member.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_member, key, value)
#     db_member.time = datetime.datetime.strftime(db_member.time, "%Y-%m-%d %H:%M:%S")
#     session.add(db_member)
#     session.commit()
#     session.refresh(db_member)
#     return True


@router.put("/update_member/{member_id}")
async def update_member(member_id: int, member=Body(...), session: Session = Depends(get_session)):
    db_member = session.get(Member, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    update_data = member
    update_data["time"] = datetime.fromisoformat(update_data["time"])
    for key, value in update_data.items():
        setattr(db_member, key, value)

    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return True
