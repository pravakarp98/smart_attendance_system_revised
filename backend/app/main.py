from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.rate_limiter import init_rate_limiter

# Import routers
from app.routes.login import router as login_router
from app.routes.signup import router as signup_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return {"Message": "Success!"}

# @app.on_event("startup")
# async def startup_event():
#     redis_url = settings.REDIS_URL  # Ensure this is defined in your settings
#     await init_rate_limiter(redis_url)

app.include_router(login_router)
app.include_router(signup_router)