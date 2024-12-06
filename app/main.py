from fastapi import FastAPI


from research.config.database import engine, Base
from research.routers import researches, users

app = FastAPI(title="Research API")

Base.metadata.create_all(bind=engine)

# app.include_router(auths.router)
app.include_router(researches.router)
app.include_router(users.router)
