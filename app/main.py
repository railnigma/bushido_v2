from fastapi import FastAPI

from app.api.tasks import router as tasks_router

app = FastAPI(
    title="Bushido Planner API",
    version="0.1.0",
    description="Simple API for managing daily tasks",
)

app.include_router(tasks_router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict:
    return {"status": "ok"}