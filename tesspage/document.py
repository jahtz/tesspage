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


def page_to_string(page: Page) -> str:
    """
    Converts page object to single string

    Args:
        page: Page object

    Returns:
        page text as string (lines seperated with \\n, textregions with \\n\\n)
    """
    return '\n\n'.join(['\n'.join([line.text for line in region.text_lines]) for region in page.text_regions])
