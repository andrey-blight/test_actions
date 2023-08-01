from fastapi import APIRouter

router = APIRouter()


@router.get("/one")
def get_one():
    return 1
