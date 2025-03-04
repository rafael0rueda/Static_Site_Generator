import sys
from textnode import *
from copy_files import clean_copy_directory 
from generate_content import generate_pages_recursive



def main():
    src_dir = "./content/"
    dest_dir = "./docs/"
    template = "./template.html"
    static = "./static"

    # Set default basepath
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    clean_copy_directory(static, dest_dir)
    generate_pages_recursive(src_dir, template, dest_dir, basepath)
    
    return

main()