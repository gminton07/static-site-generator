class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: "list[HTMLNode] | None" = None, props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        return

    def to_html(self) -> None:
        raise NotImplementedError("Implement to_html in child classes")

    def props_to_html(self) -> str:
        if self.props == None:
            return ""

        html_str = ""
        for key, value in self.props.items():
            html_str += f' {key}="{value}"'
        
        return html_str

    def __repr__(self) -> str:
        return f"""tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props};\n"""
