from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag=tag, children=children, props=props)
        pass

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode object requires 'tag' attribute")
        if self.children is None:
            raise ValueError("ParentNode object requires 'children' attribute")

        html_str = f"<{self.tag}>"
        for child in self.children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"

        return html_str
