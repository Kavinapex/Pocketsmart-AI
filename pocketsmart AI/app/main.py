from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from fastapi.responses import (
    JSONResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from starlette.middleware.sessions import (
    SessionMiddleware,
)

from starlette.staticfiles import (
    StaticFiles,
)

from app.config import get_settings

from app.database import init_db

from app.routes import (
    auth,
    pages,
    planners,
)


BASE_DIR = Path(__file__).resolve().parent

settings = get_settings()


app = FastAPI(

    title=settings.app_name,

    description=(
        "Budget-aware AI recommendations "
        "for home, party and jewelry planning."
    ),

    version="1.0.0",
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.cors_list,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.add_middleware(

    SessionMiddleware,

    secret_key=settings.secret_key,

    max_age=60 * 60 * 8,
)


app.mount(

    "/static",

    StaticFiles(
        directory=BASE_DIR / "static"
    ),

    name="static",
)


app.state.templates = Jinja2Templates(

    directory=str(
        BASE_DIR / "templates"
    )

)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)


@app.on_event("startup")
def startup():

    init_db()


@app.get("/startup")
def startup_status():

    return {

        "status": "ready",

        "app":
            settings.app_name,

        "gemini_model":
            settings.gemini_model,
    }


@app.get("/session-info")
def session_info(
    request: Request,
):

    return {

        "logged_in":
            bool(
                request.session.get(
                    "access_token"
                )
            ),

        "user_id":
            request.session.get(
                "user_id"
            ),
    }


@app.get("/session-data")
def session_data(
    request: Request,
):

    return {

        "user_id":
            request.session.get(
                "user_id"
            ),

        "has_access_token":
            bool(
                request.session.get(
                    "access_token"
                )
            ),
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }