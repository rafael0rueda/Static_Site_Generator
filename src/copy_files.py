import os
import shutil

def delete_files_in_directory(directory_path):
    files = os.listdir(directory_path)
    for file in files:
        sub_folder = os.path.join(directory_path, file)
        if os.path.isdir(sub_folder):
            shutil.rmtree(sub_folder)
        else:
            os.unlink(sub_folder)
    
    return

def clean_copy_directory(dir_src, dir_dest):
    print(f"Deleting public directory {dir_dest}...")
    delete_files_in_directory(dir_dest)
    print(f"Copy to {dir_dest} directory...")
    files = os.listdir(dir_src)
    for file in files:
        s = os.path.join(dir_src, file)
        d = os.path.join(dir_dest, file)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    return
