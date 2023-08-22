from dataclasses import dataclass, field


@dataclass()
class TextLine:
    id: str
    text: str = ''
    coords: list = field(default_factory=list)


@dataclass()
class TextRegion:
    id: str
    coords: list = field(default_factory=list)
    text_lines: list = field(default_factory=list)


@dataclass()
class Page:
    id: str
    file: str
    height: int
    width: int
    text_regions: list = field(default_factory=list)  # order in list == reading order


@dataclass
class Document:
    id: str
    file: str
    creator: str = ''
    created: str = ''
    last_change: str = ''
    pages: list = field(default_factory=list)


