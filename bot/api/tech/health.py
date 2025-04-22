from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from bot.api.tech.router import router


@router.get("/healthcheck")
async def healthcheck(request: Request) -> Response:
    return Response("Healthy", status_code=200)


@router.get("/")
async def tmp():
    return JSONResponse({"hello": "world"})