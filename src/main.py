from textnode import TextType, TextNode

def main() -> None:
    textnode = TextNode('This is bold',
                        TextType.BOLD,
                        None)
    print(textnode)

    textnode2 = TextNode('Link to youtube',
                         TextType.LINK,
                         'https://youtube.com')
    print(textnode2)

    print(f'Equal: {textnode == textnode2}')
    return

if __name__ == '__main__':
    main()
