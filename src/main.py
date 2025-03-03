from textnode import *
from copy_files import clean_copy_directory 
from block_markdown import *
import os
import shutil

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(f"{from_path}/index.md", "r") as file:
        src_markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    node = markdown_to_html_node(src_markdown)
    html = node.to_html()
    title = extract_title(src_markdown).strip()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    # If not exists, create it
    os.makedirs(os.path.dirname(f"{dest_path}/index.html"), exist_ok=True)
    with open(f"{dest_path}/index.html", "w") as file:
        file.write(template)
    return

def main():
    src_dir = "./content/"
    dest_dir = "./public/"
    template = "./template.html"
    static = "./static"
    clean_copy_directory(static, dest_dir)
    generate_page(src_dir, template, dest_dir)
    
    return

main()