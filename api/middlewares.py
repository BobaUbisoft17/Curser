from typing import Awaitable, Callable
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response


class DatabaseMiddleware:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        async with self.session() as session:
            request.state.session = session
            return await call_next(request)
