from dataclasses import dataclass, field


@dataclass()
class TextLine:
    id: str
    text: str = ''
    coords: list[list[int]] = field(default_factory=list)


@dataclass()
class TextRegion:
    id: str
    custom: str = ''
    coords: list[list[int]] = field(default_factory=list)
    text_lines: list[TextLine] = field(default_factory=list)


@dataclass()
class Page:
    id: str
    file: str
    height: int = 0
    width: int = 0
    text_regions: list[TextRegion] = field(default_factory=list)

