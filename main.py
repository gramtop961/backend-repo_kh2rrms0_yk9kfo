import os
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Soccer Data API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchSample(BaseModel):
    id: str
    date: str
    competition: str
    home_team: str
    away_team: str
    venue: str
    score: str


class PlayerSample(BaseModel):
    id: str
    name: str
    position: str
    age: int
    club: str
    nation: str


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/api/sample/matches")
def get_sample_matches() -> dict:
    """Return a few sample match summaries for the landing page."""
    items: List[MatchSample] = [
        MatchSample(
            id="ucl-2023-final",
            date="2023-06-10",
            competition="UEFA Champions League",
            home_team="Manchester City",
            away_team="Inter Milan",
            venue="Atatürk Olympic Stadium",
            score="1-0",
        ),
        MatchSample(
            id="wc-2022-final",
            date="2022-12-18",
            competition="FIFA World Cup",
            home_team="Argentina",
            away_team="France",
            venue="Lusail Stadium",
            score="3-3 (4-2 pens)",
        ),
        MatchSample(
            id="prem-2024-title-decider",
            date="2024-05-19",
            competition="Premier League",
            home_team="Manchester City",
            away_team="West Ham",
            venue="Etihad Stadium",
            score="3-1",
        ),
    ]
    return {"items": [m.model_dump() for m in items]}


@app.get("/api/sample/players")
def get_sample_players() -> dict:
    """Return a few sample player profiles for the landing page."""
    items: List[PlayerSample] = [
        PlayerSample(
            id="arg-10",
            name="Lionel Messi",
            position="RW/CF",
            age=36,
            club="Inter Miami",
            nation="Argentina",
        ),
        PlayerSample(
            id="fra-7",
            name="Kylian Mbappé",
            position="LW/CF",
            age=26,
            club="Real Madrid",
            nation="France",
        ),
        PlayerSample(
            id="nor-9",
            name="Erling Haaland",
            position="ST",
            age=25,
            club="Manchester City",
            nation="Norway",
        ),
    ]
    return {"items": [p.model_dump() for p in items]}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        # Try to import database module
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
