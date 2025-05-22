from fastapi import FastAPI

from app.api.router import router
from app.db.database import Base, engine

app = FastAPI(title="HDB insights", debug=True)

Base.metadata.create_all(bind=engine)

app.include_router(router)
