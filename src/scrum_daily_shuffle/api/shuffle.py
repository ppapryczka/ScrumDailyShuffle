import random
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from scrum_daily_shuffle.api.daddy_joke import get_newest_daddy_joke, get_random_daddy_joke
from scrum_daily_shuffle.config import CONFIG, ShuffleSitesConfig
from scrum_daily_shuffle.db import get_db_session
from scrum_daily_shuffle.utils import (
    DAILY_SHUFFLE_DADDY_JOKE_SITE_PART,
    DAILY_SHUFFLE_PATH_BASE,
    SHUFFLE_SITE,
)

shuffle_router: APIRouter = APIRouter(prefix=f"/{DAILY_SHUFFLE_PATH_BASE}")


def transform_daily_shuffle_site_template(
    ssc: ShuffleSitesConfig, db_session: Session
) -> str:
    """
    Transform HTML template into site using configuration from ``ssc``.
    """
    # team name
    site = SHUFFLE_SITE.replace("{team_name}", ssc.team_name, 2)

    # people list
    random.shuffle(ssc.people_list)
    html_people_order_str = " ".join([f"<li>{p}</li>" for p in ssc.people_list])
    site = site.replace("{people_order}", html_people_order_str, 1)

    # quote
    if ssc.quote:
        site = site.replace("{quote}", f'<aside><em>"{ssc.quote}"</em></aside>', 1)
    else:
        site = site.replace("{quote}", "", 1)

    # daddy joke
    if ssc.daddy_jokes:
        newest_joke, newest_joke_html = get_newest_daddy_joke(db_session)
        _, random_joke_html = get_random_daddy_joke(db_session, newest_joke)

        daddy_joke = DAILY_SHUFFLE_DADDY_JOKE_SITE_PART
        daddy_joke = daddy_joke.replace("{newest_joke}", newest_joke_html, 1)
        daddy_joke = daddy_joke.replace("{joke}", random_joke_html, 1)

        site = site.replace("{joke}", daddy_joke, 1)
    else:
        site = site.replace("{joke}", "", 1)

    return site


@shuffle_router.get("/{site}", response_class=HTMLResponse)
def get_team_site(
    site: str, db_session: Session = Depends(get_db_session)
) -> HTMLResponse:
    sites = CONFIG.sites_dict()
    if site in sites:
        return HTMLResponse(
            transform_daily_shuffle_site_template(sites[site], db_session)
        )
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f"Such team not exists - {site}"
        )
