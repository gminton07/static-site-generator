from enum import Enum

class TextType(Enum):
    TEXT = 'plain'
    BOLD = '**'
    ITALIC = '*'
    CODE = '`'
    LINK = '[]()'
    IMAGE = '![]()'


class TextNode():
    def __init__(self, text:str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        pass;

    def __eq__(self, other: 'TextNode') -> bool:
        if (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url):
            return True
        return False

    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
