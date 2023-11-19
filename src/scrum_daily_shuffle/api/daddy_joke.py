import random
from http import HTTPStatus
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from scrum_daily_shuffle.db import get_db_session
from scrum_daily_shuffle.model import DaddyJoke, Joke, Meme, SpoilerJoke
from scrum_daily_shuffle.schemas import (
    CreateJokeSchema,
    CreateMemeSchema,
    CreateSpoilerJokeSchema,
    JokeSchema,
    MemeSchema,
    SpoilerJokeSchema,
)
from scrum_daily_shuffle.utils import DADDY_JOKE_SITE, DADDY_JOKES_PATH

daddy_joke_router: APIRouter = APIRouter(prefix=f"/{DADDY_JOKES_PATH}")


JOKE_TEMPLATE = """
    <div id="joke" style="display:none">
        {joke}
    </div>
    <center>
        <button title="Show/hide random daddy joke" type="button"
        onclick="if(document.getElementById('joke') .style.display=='none')
        {document.getElementById('joke') .style.display=''}else{document.getElementById('joke') .style.display='none'}">
        Show/hide random daddy joke</button>
    </center>
"""

NEWEST_JOKE_TEMPLATE = """
    <div id="newest-joke" style="display:none">
        {joke}
    </div>
    <center>
        <button title="Show/hide newest daddy joke" type="button"
        onclick="if(document.getElementById('newest-joke') .style.display=='none')
        {document.getElementById('newest-joke') .style.display=''}else{document.getElementById('newest-joke') .style.display='none'}">
        Show/hide newest daddy joke</button>
    </center>
"""


def get_all_daddy_jokes(db_session: Session) -> List[DaddyJoke]:
    """
    Get all available jokes from database.
    """
    jokes = db_session.query(Meme).all()
    spoiler_jokes = db_session.query(Joke).all()
    meme = db_session.query(SpoilerJoke).all()

    return jokes + spoiler_jokes + meme  # type: ignore


def get_random_daddy_joke(
    db_session: Session, other: Optional[DaddyJoke] = None
) -> Tuple[DaddyJoke, str]:
    """
    Get random joke and its HTML representation. If ``other`` given it
    cannot be same daddy joke as ``other``.
    """
    daddy_jokes = get_all_daddy_jokes(db_session)

    if other:
        # we don't want to have same jokes
        daddy_jokes = [d for d in daddy_jokes if d != other]

        # two spoiler jokes will be a problem as spoiler button
        # will only show spoiler for first joke, because of same
        # HTML id - just omit all spoiler jokes if one already used
        if isinstance(other, SpoilerJoke):
            daddy_jokes = [d for d in daddy_jokes if not isinstance(d, SpoilerJoke)]

    daddy_jokes = daddy_jokes
    chosen = random.choice(daddy_jokes)
    return chosen, chosen.get_html_representation(JOKE_TEMPLATE)


def get_newest_daddy_joke(db_session: Session) -> Tuple[DaddyJoke, str]:
    """
    Get newest available daddy joke.
    """
    daddy_jokes = get_all_daddy_jokes(db_session)
    daddy_jokes.sort(key=lambda x: x.creation_date, reverse=True)
    return daddy_jokes[0], daddy_jokes[0].get_html_representation(NEWEST_JOKE_TEMPLATE)


@daddy_joke_router.get("", response_class=HTMLResponse)
def get_random_daddy_joke_site(db_session: Session = Depends(get_db_session)) -> str:
    _, joke_html = get_random_daddy_joke(db_session)

    return DADDY_JOKE_SITE.replace("{joke}", joke_html, 1)


@daddy_joke_router.get("/jokes", response_model=List[JokeSchema])
def get_jokes(db_session: Session = Depends(get_db_session)) -> List[JokeSchema]:
    """
    Get all jokes.
    """
    jokes = db_session.query(Joke).all()
    return jokes  # type: ignore


@daddy_joke_router.get("/spoiler_jokes", response_model=List[SpoilerJokeSchema])
def get_spoiler_jokes(
    db_session: Session = Depends(get_db_session),
) -> List[SpoilerJokeSchema]:
    """
    Get all spoiler jokes.
    """
    spoiler_jokes = db_session.query(SpoilerJoke).all()
    return spoiler_jokes  # type: ignore


@daddy_joke_router.get("/memes", response_model=List[MemeSchema])
def get_memes(
    db_session: Session = Depends(get_db_session),
) -> List[MemeSchema]:
    """
    Get all memes.
    """
    memes = db_session.query(Meme).all()
    return memes  # type: ignore


@daddy_joke_router.post("/jokes", response_model=JokeSchema)
def create_joke(
    data: CreateJokeSchema, db_session: Session = Depends(get_db_session)
) -> JokeSchema:
    """
    Create new joke.
    """
    joke = Joke(joke=data.joke)
    db_session.add(joke)
    db_session.commit()
    db_session.refresh(joke)

    return joke  # type: ignore


@daddy_joke_router.post("/spoiler_jokes", response_model=SpoilerJokeSchema)
def create_spoiler_joke(
    data: CreateSpoilerJokeSchema, db_session: Session = Depends(get_db_session)
) -> SpoilerJokeSchema:
    """
    Create new spoiler joke.
    """
    spoiler_joke = SpoilerJoke(joke=data.joke, spoiler=data.spoiler)
    db_session.add(spoiler_joke)
    db_session.commit()
    db_session.refresh(spoiler_joke)

    return spoiler_joke  # type: ignore


@daddy_joke_router.post("/memes", response_model=MemeSchema)
def create_meme(
    data: CreateMemeSchema, db_session: Session = Depends(get_db_session)
) -> MemeSchema:
    """
    Create new meme.
    """
    meme = Meme(link=data.link)
    db_session.add(meme)
    db_session.commit()
    db_session.refresh(meme)

    return meme  # type: ignore


@daddy_joke_router.delete("/jokes/{id}", response_model=None)
def delete_joke(id: int, db_session: Session = Depends(get_db_session)) -> Response:
    """
    Delete joke by ``id``.
    """
    joke = db_session.query(Joke).filter(Joke.id == id).first()

    if not joke:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Joke not found.")

    db_session.delete(joke)
    db_session.commit()

    return Response(status_code=HTTPStatus.NO_CONTENT)


@daddy_joke_router.delete("/spoiler_jokes/{id}", response_model=None)
def delete_spoiler_joke(
    id: int, db_session: Session = Depends(get_db_session)
) -> Response:
    """
    Delete spoiler joke by ``id``.
    """
    spoiler_joke = db_session.query(SpoilerJoke).filter(SpoilerJoke.id == id).first()

    if not spoiler_joke:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Spoiler joke not found."
        )

    db_session.delete(spoiler_joke)
    db_session.commit()

    return Response(status_code=HTTPStatus.NO_CONTENT)


@daddy_joke_router.delete("/memes/{id}", response_model=None)
def delete_meme(id: int, db_session: Session = Depends(get_db_session)) -> Response:
    """
    Delete meme by ``id``.
    """

    meme = db_session.query(Meme).filter(Meme.id == id).first()

    if not meme:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Meme not found.")

    db_session.delete(meme)
    db_session.commit()

    return Response(status_code=HTTPStatus.NO_CONTENT)
