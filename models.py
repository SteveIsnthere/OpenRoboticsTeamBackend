from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from typing import Optional, List
from datetime import datetime
from faker import Faker
import random

faker = Faker()


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

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)

# # Function to create dummy data
# def create_dummy_data():
#     with Session(engine) as session:
#         for _ in range(10):
#             project = Project(
#                 name=faker.company(),
#                 is_robo_cup=faker.boolean(),
#                 is_completed=faker.boolean(),
#                 description=faker.text(),
#                 image="https://material.angular.io/assets/img/examples/shiba2.jpg",
#                 github=faker.url(),
#                 weblink=faker.url(),
#                 time=faker.date_time_this_decade()
#             )
#             session.add(project)
#             session.commit()
#
#             for _ in range(3):
#                 subteam = Subteam(
#                     name=faker.bs(),
#                     project_id=project.id
#                 )
#                 session.add(subteam)
#                 session.commit()
#
#                 for _ in range(5):
#                     member = Member(
#                         name=faker.name(),
#                         is_captain=faker.boolean(),
#                         is_retired=faker.boolean(),
#                         discipline=faker.job(),
#                         bio=faker.text(),
#                         image="https://material.angular.io/assets/img/examples/shiba2.jpg",
#                         email=faker.email(),
#                         github=faker.url(),
#                         linkedin=faker.url(),
#                         weblink=faker.url(),
#                         time=faker.date_time_this_decade()
#                     )
#                     session.add(member)
#                     session.commit()
#
#                     subteam_role = SubteamRole(
#                         name=faker.job(),
#                         subteam_id=subteam.id,
#                         member_id=member.id
#                     )
#                     session.add(subteam_role)
#                     session.commit()
#
#                     # Adding ProjectRole for each member in the project
#                     project_role = ProjectRole(
#                         is_lead=faker.boolean(),
#                         is_colead=faker.boolean(),
#                         name=faker.job(),
#                         project_id=project.id,
#                         member_id=member.id
#                     )
#                     session.add(project_role)
#                     session.commit()
#
#         session.commit()
#
# # Create the dummy data
# create_dummy_data()
