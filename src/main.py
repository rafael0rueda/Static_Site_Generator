from textnode import *
from copy_files import clean_copy_directory 
from generate_content import generate_page, generate_pages_recursive

def main():
    src_dir = "./content/"
    dest_dir = "./public/"
    template = "./template.html"
    static = "./static"
    clean_copy_directory(static, dest_dir)
    # generate_page(src_dir, template, dest_dir)
    generate_pages_recursive(src_dir, template, dest_dir)
    
    return

main()