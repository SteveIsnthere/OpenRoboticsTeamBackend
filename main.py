from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.members import router as members

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200",
                   "https://nlp-voice.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(members, prefix="/members")


@app.get("/")
def read_root():
    return {"Hello": "World"}
