from dataclasses import dataclass, field

@dataclass
class MangaInfo:
    cid: str
    title: str
    cover: str | None = None
    author: str | None = None
    chapters: dict[str, dict[str, str | list[str]]] = field(default_factory=dict)