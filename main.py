from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# ✅ Your assigned API key
API_KEY = "ak_no6r9p7ajl0y61ajab7sd1sv"

# ✅ Allow CORS (important for grader browser check)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Input format
class Event(BaseModel):
    user: str
    amount: float
    ts: int

class RequestBody(BaseModel):
    events: List[Event]


# 🚀 POST endpoint
@app.post("/analytics")
def analytics(data: RequestBody, x_api_key: Optional[str] = Header(None)):

    # 🔐 Step 1: check API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = data.events

    # 📊 Step 2: total events
    total_events = len(events)

    # 👥 Step 3: unique users
    users = set(e.user for e in events)
    unique_users = len(users)

    # 💰 Step 4: revenue (only positive amounts)
    revenue = sum(e.amount for e in events if e.amount > 0)

    # 🏆 Step 5: top user (highest positive sum)
    user_totals = {}

    for e in events:
        if e.amount > 0:
            user_totals[e.user] = user_totals.get(e.user, 0) + e.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None

    # 📤 Step 6: response
    return {
        "email": "23f2004096@ds.study.iitm.ac.in",  # replace this
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }