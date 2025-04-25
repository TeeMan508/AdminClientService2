from starlette.responses import Response, JSONResponse

from bot.api.tech.router import router

from bot.schemas.send_to_service_request import SendToServiceRequest
from bot.utils.send_to_service import send_to_service


# for tests
@router.post("/send_to_service")
async def send_to_service_(request: SendToServiceRequest) -> Response:
    await send_to_service(request)
    return JSONResponse({}, status_code=200)

