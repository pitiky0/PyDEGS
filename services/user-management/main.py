from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routes import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "you are in the root path of the User Management API"}

