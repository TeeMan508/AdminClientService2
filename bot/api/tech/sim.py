from starlette.responses import Response

from bot.api.tech.router import router

from bot.schemas.send_to_service_request import SendToServiceRequest
from bot.utils.send_to_service import send_to_service


# for tests
@router.post("/send_to_service")
async def healthcheck(request: SendToServiceRequest) -> Response:
    await send_to_service(request)
    return Response({}, status_code=200)

