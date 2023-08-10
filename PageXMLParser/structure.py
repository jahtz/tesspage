from dataclasses import dataclass, field
from numpy import ndarray


@dataclass
class Line:
    """Line data object"""
    id: str
    text: str
    coords: ndarray


@dataclass
class Page:
    """Page data object"""
    file: str
    height: int
    width: int
    lines: list[Line] = field(default_factory=list)


@dataclass
class PageXML:
    """PageXML data object"""
    id: str
    pages: list[Page] = field(default_factory=list)
