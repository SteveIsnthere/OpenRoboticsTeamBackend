from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.members import router as members
from routes.projects import router as projects
from routes.overview import router as overview

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200",
                   "https://open-robotics-team.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(members, prefix="/members")
app.include_router(projects, prefix="/projects")
app.include_router(overview, prefix="/overview")


@app.get("/")
def read_root():
    return {"Hello": "World"}
