from typing import Dict, List, Optional

from prettytable import PrettyTable  # type: ignore
from pydantic import BaseModel, BaseSettings


class ShuffleSitesConfig(BaseModel):
    team_name: str
    site_path: str
    people_list: List[str]
    daddy_jokes: bool = False
    quote: Optional[str] = None


class Config(BaseSettings):
    href_base: str
    shuffle_sites_configs: List[ShuffleSitesConfig]
    sqlite3_filepath: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def to_pretty_table(self) -> str:
        """
        Converts configuration fields into pretty table, so pretty that you
        can print it!
        """
        dictionary = self.dict()
        dictionary = {key.upper(): value for key, value in dictionary.items()}
        table = PrettyTable(["key", "value"])
        for key, val in dictionary.items():
            table.add_row([key, val])
        return table.get_string()

    def sites_dict(self) -> Dict[str, ShuffleSitesConfig]:
        return {s.site_path: s for s in self.shuffle_sites_configs}


CONFIG: Config = Config()
