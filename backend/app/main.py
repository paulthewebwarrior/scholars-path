import logging
import time
from uuid import uuid4

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .database import Base, engine
from .routers.auth import router as auth_router
from .routers.habits import router as habits_router
from .routers.profile import router as profile_router

settings = get_settings()
logger = logging.getLogger('app')

app = FastAPI(title='Auth Profile API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    )


configure_logging()


@app.middleware('http')
async def request_logging_middleware(request: Request, call_next):
    request_id = request.headers.get('x-request-id') or str(uuid4())
    started = time.perf_counter()
    logger.info(
        'request.start request_id=%s method=%s path=%s query=%s client=%s',
        request_id,
        request.method,
        request.url.path,
        request.url.query,
        request.client.host if request.client else 'unknown',
    )
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - started) * 1000
        logger.exception(
            'request.error request_id=%s method=%s path=%s duration_ms=%.2f',
            request_id,
            request.method,
            request.url.path,
            duration_ms,
        )
        return JSONResponse(
            status_code=500,
            content={'detail': 'Internal server error', 'request_id': request_id},
            headers={'X-Request-ID': request_id},
        )

    duration_ms = (time.perf_counter() - started) * 1000
    logger.info(
        'request.end request_id=%s method=%s path=%s status=%s duration_ms=%.2f',
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers['X-Request-ID'] = request_id
    return response


@app.on_event('startup')
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info('startup db.initialized database_url=%s', settings.database_url)
    routes = sorted(
        {
            f"{','.join(sorted(route.methods or []))} {route.path}"
            for route in app.routes
            if getattr(route, 'path', None)
        }
    )
    for route in routes:
        logger.info('startup route.registered %s', route)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(habits_router)
