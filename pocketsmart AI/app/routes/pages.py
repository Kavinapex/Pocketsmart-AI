from fastapi import APIRouter

router = APIRouter(
    tags=["Pages"],
)


@router.get("/")
def home():
    return {
        "message": "Welcome to PocketSmart AI"
    }