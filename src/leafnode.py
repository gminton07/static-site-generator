from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode objects must have 'value' attribute")

        if self.tag is None:
            return self.value
        
        html_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_str

    def __repr__(self) -> str:
        return f'tag: {self.tag}\tvalue: {self.value}\tprops: {self.props}'
