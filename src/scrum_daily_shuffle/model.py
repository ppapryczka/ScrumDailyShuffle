from abc import abstractmethod

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

BASE = declarative_base()


class DaddyJoke(BASE):
    __abstract__ = True

    def get_html_representation(self, template: str) -> str:
        joke = self._get_joke()
        return template.replace("{joke}", joke, 1)

    @abstractmethod
    def _get_joke(self) -> str:
        pass


class Joke(DaddyJoke):
    __tablename__ = "joke"
    id = Column(Integer, primary_key=True)
    joke = Column(String)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    def _get_joke(self) -> str:
        joke = " ".join([f"{line} </br>" for line in self.joke.splitlines()])
        return joke


class SpoilerJoke(DaddyJoke):
    __tablename__ = "spoiler_joke"
    id = Column(Integer, primary_key=True)
    joke = Column(String)
    spoiler = Column(String)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    def _get_joke(self) -> str:
        joke = """
            {joke}
        <div id="spoiler" style="display:none">
            {spoiler}
        </div>
            <button title="Show/hide spoiler" type="button"
            onclick="if(document.getElementById('spoiler') .style.display=='none')
            {document.getElementById('spoiler') .style.display=''}else{document.getElementById('spoiler') .style.display='none'}">
            Show/hide spoiler</button>
        </div>
        """

        # replace fields
        joke = joke.replace(
            "{joke}", " ".join([f"{line} </br>" for line in self.joke.splitlines()]), 1
        )
        joke = joke.replace("{spoiler}", self.spoiler, 1)

        return joke


class Meme(DaddyJoke):
    __tablename__ = "meme"

    id = Column(Integer, primary_key=True)
    link = Column(String)

    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    def _get_joke(self) -> str:
        return f'<img src="{self.link}"/>'
