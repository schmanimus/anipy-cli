from dataclasses import dataclass, field
from time import time
from dataclasses_json import dataclass_json, config
from typing import Dict, Optional

from anipy_cli.config import Config
from anipy_cli.provider import Episode
from anipy_cli.anime import Anime

# TODO: History migration

@dataclass_json
@dataclass
class HistoryEntry:
    provider: str = field(metadata=config(field_name="pv"))
    identifier: str = field(metadata=config(field_name="id"))
    name: str = field(metadata=config(field_name="na"))
    episode: Episode = field(metadata=config(field_name="ep"))
    timestamp: int = field(metadata=config(field_name="ts"))

    def __repr__(self) -> str:
        return f"{self.name} Episode {self.episode}"


@dataclass_json
@dataclass
class History:
    history: Dict[str, HistoryEntry]


def get_history() -> Dict[str, HistoryEntry]:
    hist_file = Config().history_file_path

    if not hist_file.is_file():
        return {}
        
    history = History.from_json(hist_file.read_text())

    return history.history


def get_history_entry(anime: Anime) -> Optional[HistoryEntry]:
    history = get_history()
    uniqueid = f"{anime.provider.NAME}:{anime.identifier}"

    return history.get(uniqueid, None)


def update_history(anime: Anime, episode: Episode):
    hist_file = Config().history_file_path
    history = get_history()
    
    uniqueid = f"{anime.provider.NAME}:{anime.identifier}"
    entry = history.get(uniqueid, None)

    if entry is None:
        entry = HistoryEntry(
            provider=anime.provider.NAME, 
            identifier=anime.identifier, 
            name=anime.name, 
            episode=episode, 
            timestamp=int(time())
        )
        history[uniqueid] = entry
    else:
        entry.episode = episode
        entry.timestamp = int(time())
        history[uniqueid] = entry

    hist_file.write_text(History(history=history).to_json())
