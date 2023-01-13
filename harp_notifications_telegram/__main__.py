import harp_notifications_telegram.settings as settings
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from harp_notifications_telegram.api.health import router as health
from harp_notifications_telegram.api.notification_profile import router as notification_profile
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    openapi_url=f'{settings.URL_PREFIX}/openapi.json',
    docs_url=f'{settings.URL_PREFIX}/docs',
    redoc_url=f'{settings.URL_PREFIX}/redoc'
)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)
app.include_router(health)
app.include_router(notification_profile)
