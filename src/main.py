import shutil
import  os
from textnode import *

dir_path_static = "./static"
dir_path_public = "./public"

def copy_static_to_public():
    print("Deleting public directory...")
    shutil.rmtree(dir_path_public)
    print("Copying static files to public directory...")
    shutil.copytree(dir_path_static, dir_path_public)

def extract_title(markdown):
    pass

def main():
    copy_static_to_public()

main()
