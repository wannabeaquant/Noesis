from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/subscribe")
def subscribe():
    # Placeholder: Add subscriber
    return {"status": "subscribed"}

@router.post("/unsubscribe")
def unsubscribe():
    # Placeholder: Remove subscriber
    return {"status": "unsubscribed"} 