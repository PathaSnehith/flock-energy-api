
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from app.client import PortalClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.portal = PortalClient()
    yield


app = FastAPI(
    title="Flock Energy Meter API",
    description="API for Urja Meter Ops",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}


@app.get("/api/meters", tags=["Meters"])
async def list_meters(
    search: str = Query(default=""),
    page: int = Query(default=1, ge=1),
):
    try:
        return await app.state.portal.search_meters(
            query=search,
            page=page,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Portal request failed: {exc}",
        ) from exc


@app.get("/api/meters/{meter_id}/consumption", tags=["Meters"])
async def get_meter_consumption(meter_id: str):
    try:
        return await app.state.portal.get_meter_energy(meter_id)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Portal request failed: {exc}",
        ) from exc
