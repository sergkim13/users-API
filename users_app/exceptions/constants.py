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
