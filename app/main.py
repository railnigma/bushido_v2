from fastapi import FastAPI

app = FastAPI(
    title="Bushido Planner",
    version="0.1.0",
    description="Planner for real Samurai"
)


@app.get("/health", tags=["health"])
def healthcheck() -> dict:
    return {"status": "ok"}