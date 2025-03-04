from block_markdown import markdown_to_html_node, extract_title
import os
import pathlib


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(f"{from_path}", "r") as file:
        src_markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    node = markdown_to_html_node(src_markdown)
    html = node.to_html()
    title = extract_title(src_markdown).strip()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace("href='/", "href='" + basepath)
    template = template.replace("src='/", "src='" + basepath)
    # If not exists, create it 
    os.makedirs(os.path.dirname(f"{dest_path}/index.html"), exist_ok=True)
    with open(f"{dest_path}/index.html", "w") as file:
        file.write(template)
    
    return

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file == "index.md":
                file_path = os.path.relpath(os.path.join(root,file))
                des_temp = os.path.relpath(root)
                des_path = dest_dir_path + "/" + des_temp.replace("content", "")
                generate_page(file_path, template_path, des_path, basepath)
                
    return

