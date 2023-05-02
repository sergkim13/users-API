from users_app.validation.schemas import CodelessErrorResponseModel, ErrorResponseModel

E400 = {
    400: {'description': 'Bad Request', 'model': ErrorResponseModel},
}
E400_401 = {
    400: {'description': 'Bad Request', 'model': ErrorResponseModel},
    401: {'description': 'Unauthorized', 'model': CodelessErrorResponseModel},
}
E401_403 = {
    401: {'description': 'Unauthorized', 'model': CodelessErrorResponseModel},
    403: {'description': 'Forbidden', 'model': CodelessErrorResponseModel},
}
E400_401_403 = {
    400: {'description': 'Bad Request', 'model': ErrorResponseModel},
    401: {'description': 'Unauthorized', 'model': CodelessErrorResponseModel},
    403: {'description': 'Forbidden', 'model': CodelessErrorResponseModel},
}
E400_401_404 = {
    400: {'description': 'Bad Request', 'model': ErrorResponseModel},
    401: {'description': 'Unauthorized', 'model': CodelessErrorResponseModel},
    404: {'description': 'Not Found', 'model': CodelessErrorResponseModel},
}
E400_401_403_404 = {
    400: {'description': 'Bad Request', 'model': ErrorResponseModel},
    401: {'description': 'Unauthorized', 'model': CodelessErrorResponseModel},
    403: {'description': 'Forbidden', 'model': CodelessErrorResponseModel},
    404: {'description': 'Not Found', 'model': CodelessErrorResponseModel},
}

# Messages
MSG_NOT_AUTHENTICATED = 'You are not authentificated. Please log in.'
MSG_NOT_AUTHORIZED = 'You have no permissions.'
MSG_INVALID_CREDS = 'Invalid login or password.'
MSG_EMAIL_EXISTS = 'User with email {email} already exists.'
MSG_CITY_NOT_FOUND = 'City with given ID not found.'
MSG_USER_NOT_FOUND = 'User not found.'
