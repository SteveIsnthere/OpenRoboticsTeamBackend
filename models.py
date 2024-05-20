from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from typing import Optional, List
from datetime import datetime
import random


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    is_robo_cup: bool = Field(nullable=False)
    is_completed: bool = Field(nullable=False)
    description: Optional[str] = None
    image: Optional[str] = Field(max_length=255, default=None)
    github: Optional[str] = Field(max_length=255, default=None)
    weblink: Optional[str] = Field(max_length=255, default=None)
    time: datetime = Field(default_factory=datetime.utcnow)
    subteams: List["Subteam"] = Relationship(back_populates="project")
    project_roles: List["ProjectRole"] = Relationship(back_populates="project")


class Member(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    is_captain: bool = Field(nullable=False)
    is_retired: bool = Field(nullable=False)
    discipline: Optional[str] = Field(max_length=255, default=None)
    bio: Optional[str] = None
    image: Optional[str] = Field(max_length=255, default=None)
    email: Optional[str] = Field(max_length=255, default=None)
    github: Optional[str] = Field(max_length=255, default=None)
    linkedin: Optional[str] = Field(max_length=255, default=None)
    weblink: Optional[str] = Field(max_length=255, default=None)
    time: datetime = Field(default_factory=datetime.utcnow)
    project_roles: List["ProjectRole"] = Relationship(back_populates="member")
    subteam_roles: List["SubteamRole"] = Relationship(back_populates="member")


class ProjectRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_lead: bool = Field(nullable=False)
    is_colead: bool = Field(nullable=False)
    name: Optional[str] = Field(max_length=255, default=None)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", nullable=False)
    member_id: Optional[int] = Field(default=None, foreign_key="member.id", nullable=False)
    project: "Project" = Relationship(back_populates="project_roles")
    member: "Member" = Relationship(back_populates="project_roles")


class Subteam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", nullable=False)
    project: "Project" = Relationship(back_populates="subteams")
    subteam_roles: List["SubteamRole"] = Relationship(back_populates="subteam")


class SubteamRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(max_length=255, default=None)
    subteam_id: Optional[int] = Field(default=None, foreign_key="subteam.id", nullable=False)
    member_id: Optional[int] = Field(default=None, foreign_key="member.id", nullable=False)
    subteam: "Subteam" = Relationship(back_populates="subteam_roles")
    member: "Member" = Relationship(back_populates="subteam_roles")


# Database setup

# sqlite_url = "sqlite:///database.db"
# engine = create_engine(sqlite_url)
#
# SQLModel.metadata.create_all(engine)
#


# # Dummy data

# # Function to generate random boolean
# def random_bool():
#     return bool(random.getrandbits(1))
#
#
# # Function to generate random string
# def random_string(length=10):
#     letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     return ''.join(random.choice(letters) for i in range(length))
#
#
# # Function to generate random datetime
# def random_datetime():
#     return datetime.now()
#
#
# # Creating and inserting dummy data
# with Session(engine) as session:
#     # Create dummy Projects
#     for _ in range(10):
#         project = Project(
#             name=random_string(10),
#             is_robo_cup=random_bool(),
#             is_completed=random_bool(),
#             description=random_string(50),
#             image=random_string(10),
#             github=random_string(10),
#             weblink=random_string(10),
#             time=random_datetime()
#         )
#         session.add(project)
#
#     # Create dummy Members
#     for _ in range(10):
#         member = Member(
#             name=random_string(10),
#             is_captain=random_bool(),
#             is_retired=random_bool(),
#             discipline=random_string(10),
#             bio=random_string(50),
#             image=random_string(10),
#             email=random_string(10) + "@example.com",
#             github=random_string(10),
#             linkedin=random_string(10),
#             weblink=random_string(10),
#             time=random_datetime()
#         )
#         session.add(member)
#
#     session.commit()
#
#     # Create dummy ProjectRoles
#     for _ in range(10):
#         project_role = ProjectRole(
#             is_lead=random_bool(),
#             is_colead=random_bool(),
#             name=random_string(10),
#             project_id=random.randint(1, 10),
#             member_id=random.randint(1, 10)
#         )
#         session.add(project_role)
#
#     # Create dummy Subteams
#     for _ in range(10):
#         subteam = Subteam(
#             name=random_string(10),
#             project_id=random.randint(1, 10)
#         )
#         session.add(subteam)
#
#     session.commit()
#
#     # Create dummy SubteamRoles
#     for _ in range(10):
#         subteam_role = SubteamRole(
#             name=random_string(10),
#             subteam_id=random.randint(1, 10),
#             member_id=random.randint(1, 10)
#         )
#         session.add(subteam_role)
#
#     session.commit()
