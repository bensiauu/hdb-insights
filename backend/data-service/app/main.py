from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.db.database import Base, engine

app = FastAPI(title="HDB insights", debug=True)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


Base.metadata.create_all(bind=engine)

app.include_router(router)
