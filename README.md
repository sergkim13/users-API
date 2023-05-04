# Users API (FastApi)

[![Maintainability](https://api.codeclimate.com/v1/badges/d995c9ecea3af7f1c33f/maintainability)](https://codeclimate.com/github/sergkim13/users_API/maintainability)
[![Linters check](https://github.com/sergkim13/users_API/actions/workflows/linters_check.yml/badge.svg)](https://github.com/sergkim13/users_API/actions/workflows/linters_check.yml)
[![Test coverage](https://api.codeclimate.com/v1/badges/d995c9ecea3af7f1c33f/test_coverage)](https://codeclimate.com/github/sergkim13/users_API/test_coverage)

### Description:
Users API allows you to get information about users. Includes authentication and authorizaion by JWT.
Made with:
- FastAPI,
- PostgreSQL,
- SQLAlchemy 2.0,
- Pydantic,
- Alembic,
- Docker,
- Redis.

### Requirements:
1. MacOS (prefer) / Linux / Windows10
2. `Docker`
3. `Make` utily for MacOS, Linux.

### Install:
1. Clone repository: https://github.com/sergkim13/users_API
2. Type `make compose` for running application in docker container. App will be running at http://0.0.0.0:8000. Type `make stop` to stop app container.
3. Type `make compose-test` for running tests in docker container. Type `make stop-test` to stop app container.
4. For checking `pre-commit hooks` you need `Poetry` and install dependencies:
    - `make install` (`Poetry`) or `pip install -r requirements.txt`  to install dependencies to your virtual environment.
    - `make hooks`
