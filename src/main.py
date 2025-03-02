from textnode import *
from copy_files import clean_copy_directory

def main():
    src_dir = "./static"
    dest_dir = "./public"
    clean_copy_directory(src_dir, dest_dir)
    new_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(new_node)
    return

main()