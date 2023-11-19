import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from scrum_daily_shuffle.api.daddy_joke import daddy_joke_router
from scrum_daily_shuffle.api.shuffle import shuffle_router
from scrum_daily_shuffle.config import CONFIG
from scrum_daily_shuffle.utils import get_home_site

APP: FastAPI = FastAPI(title="Daily random people order", version="0.1.0")

APP.include_router(shuffle_router)
APP.include_router(daddy_joke_router)


@APP.get("/", response_class=HTMLResponse)
def home():
    """
    Render simple home site.
    """
    return get_home_site(CONFIG)


if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=15015)
