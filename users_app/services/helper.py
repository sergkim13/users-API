
from fastapi import Depends, HTTPException, Request
from users_app.schemas.schemas import Payload

from users_app.security.cifer import Cifer, get_cifer


def get_jwt(request: Request, cifer: Cifer = Depends(get_cifer)) -> Payload:
    session_token = request.cookies.get('jwt_token')
    if not session_token:
        raise HTTPException(status_code=401, detail='You are not authentificated. Please log in.')
    payload = cifer.decode(session_token)
    print('AAAA', payload)
    return payload


def get_jwt_private(request: Request, cifer: Cifer = Depends(get_cifer)) -> Payload:
    payload = get_jwt(request, cifer)
    if not payload.get('is_admin'):
        raise HTTPException(status_code=403, detail='You have no permissions.')
    return payload
