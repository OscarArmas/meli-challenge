from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from loguru import logger


router = APIRouter(prefix='/health-check')

@router.get('/')
async def health_check():
    return JSONResponse(content={"message": "it's alive!"}, status_code=200)
