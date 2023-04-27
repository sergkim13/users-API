from fastapi import FastAPI


app = FastAPI(
    title="Users API",
    description="Users API, powered by FastAPI",
    version="0.1.0",
    docs_url="/api/v1/openapi",
    redoc_url="/api/v1/redoc",
)
