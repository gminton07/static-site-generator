import os, shutil
from textnode import TextType, TextNode
from markdown_to_blocks import markdown_to_html_node

def copy_directory(src: str, dest: str) -> None:
    # Get relative directories
    src_relpath = os.path.relpath(src)
    dest_relpath = os.path.relpath(dest)

    print(f"Copying: {src_relpath} --> {dest_relpath}")

    if os.path.exists(dest):
        print(f"Cleaning dir: {dest}")
        shutil.rmtree(dest)

    print(f"Creating dir: {dest}")
    os.mkdir(dest)

    files = os.listdir(src)
    for file in files:
        src_path = os.path.join(src_relpath, file)
        dest_path = os.path.join(dest_relpath, file)
        print(f"Copy: {src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            copy_path = shutil.copy(src_path, dest_path)
            if not os.path.exists(copy_path):
                raise Exception(f"Error: {dest_path} not created")
        elif os.path.isdir(src_path):
            copy_directory(os.path.join(src_relpath, file), os.path.join(dest_relpath, file))

    return

def extract_title(markdown: str) -> str:
    first_block = markdown.split("\n\n", 1)[0]
    if first_block.startswith("# "):
        return first_block.removeprefix("# ").strip()
    else:
        raise Exception("Error: markdown string must begin with h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    # Get file contents
    md_file = open(from_path)
    md_content = md_file.read()
    template_file = open(template_path)
    template_content = template_file.read()

    # Close files
    md_file.close()
    template_file.close()

    # Convert Markdown -> HTML
    html_node = markdown_to_html_node(md_content)
    html_string = html_node.to_html()

    # Get Title
    title = extract_title(md_content)

    # Replace template placeholders
    dest_content = template_content.replace("{{ Title }}", title)
    dest_content = template_content.replace("{{ Content }}", html_string)

    # Write HTML page to dest_path
    if os.path.exists(os.path.dirname(dest_path)):
        pass
    else:
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w') as f:
        f.write(dest_content)

    return



def main() -> None:
    copy_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    return

if __name__ == '__main__':
    main()
