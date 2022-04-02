# ===================== Importing FastAPI necessary packages =============
from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from src.routes.root import router


# ------------------ FastAPI variable ----------------------------------
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

app.include_router(router, prefix='/api/v1')
