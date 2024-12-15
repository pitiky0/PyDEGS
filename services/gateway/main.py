from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.alignment import alignment_router
from routes.auth import auth_router
from routes.files import files_router
from routes.filtering import filtering_router
from routes.quality import quality_router
from routes.quantification import quantification_router
from routes.diffexpr import diffexpr_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(files_router)
app.include_router(quality_router)
app.include_router(filtering_router)
app.include_router(alignment_router)
app.include_router(quantification_router)
app.include_router(diffexpr_router)