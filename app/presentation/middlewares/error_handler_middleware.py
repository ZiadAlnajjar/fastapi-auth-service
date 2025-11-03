import logging
from uuid import uuid4

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_401_UNAUTHORIZED

from app.domain.exceptions.already_exists_exception import AlreadyExistsException
from app.domain.exceptions.base import DomainException
from app.domain.exceptions.not_found_exception import NotFoundException
from app.modules.auth.domain.exceptions.invalid_credentials import InvalidCredentials
from app.modules.auth.domain.exceptions.token_exception import TokenException

logger = logging.getLogger(__name__)

EXCEPTION_STATUS_MAP = {
    NotFoundException: HTTP_404_NOT_FOUND,
    AlreadyExistsException: HTTP_400_BAD_REQUEST,
    ValidationError: HTTP_400_BAD_REQUEST,
    InvalidCredentials: HTTP_401_UNAUTHORIZED,
}


def _get_status_from_exception(e: Exception) -> int:
    for e_type, status in EXCEPTION_STATUS_MAP.items():
        if isinstance(e, e_type):
            return status
    return HTTP_500_INTERNAL_SERVER_ERROR


def _get_error_message(e_type: str, e: Exception, trace_id: str) -> str:
    return f"[{e_type}] {e.__class__.__name__}: {str(e)} (trace={trace_id})"


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid4())
        request.state.trace_id = trace_id

        status_code: int
        error: Exception | str

        try:
            response = await call_next(request)
            response.headers["X-Trace-Id"] = trace_id
            return response

        except (
                HTTPException,
                DomainException,
                ValidationError,
        ) as e:
            logger.info(_get_error_message("Domain Error", e, trace_id))
            status_code = _get_status_from_exception(e)
            error_msg = str(e)

        except(
                ExpiredSignatureError,
                JWTClaimsError,
                JWTError,
                TokenException,
        ) as e:
            logger.info(_get_error_message("JWT Exception", e, trace_id))
            status_code = HTTP_401_UNAUTHORIZED
            error_msg = "Invalid or expired token."

        except Exception as e:
            logger.exception(_get_error_message("Unhandled Exception", e, trace_id))
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            error_msg = "Internal Server Error"

        return JSONResponse(
            status_code=status_code,
            content={
                "error": error_msg,
            },
        )
