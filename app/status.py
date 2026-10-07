# from fastapi import FASTAPI
from fastapi import APIRouter

router = APIRouter(prefix="/statusAPIs")

@router.get("/isOk")
def healthName():
    return {"status": "I am very good from health prefix"}


@router.get("/isActive")
def healthName():
    return {"status": "No I am not"}