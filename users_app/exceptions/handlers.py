from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from users_app.validation.schemas import CodelessErrorResponseModel, ErrorResponseModel


class InternalExceptionHandler:
    '''Custom internal exceptions handler.'''

    def __call__(self, request: Request, exc: Exception):
        '''Returns `JSONResponse` with a specific message.'''
        return JSONResponse(content='Что-то пошло не так, мы уже исправляем эту ошибку.', status_code=500)


class ClientExceptionHandler:
    '''Custom client exceptions handler.'''

    def __call__(self, request: Request, exc: HTTPException):
        '''Returns `ErrorResponseModel` or `CodelessErrorResponseModel` depending on exception's code.'''
        if exc.status_code == HTTPStatus.BAD_REQUEST:
            error_response = ErrorResponseModel(code=exc.status_code.value, message=exc.detail)
            return JSONResponse(content=error_response.dict(), status_code=exc.status_code)
        if exc.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND):
            error_response = CodelessErrorResponseModel(message=exc.detail)
            return JSONResponse(content=error_response.dict(), status_code=exc.status_code)
        return exc
