import shutil
import  os
from generatepage import generate_pages_recursive, generate_page
from textnode import *

dir_path_static = "./static"
dir_path_public = "./public"
template_path ="./template.html"
dir_path_content = "./content"

def copy_static_to_public():
    print("Deleting public directory...")
    shutil.rmtree(dir_path_public)
    print("Copying static files to public directory...")
    shutil.copytree(dir_path_static, dir_path_public)

def main():
    copy_static_to_public()
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)
    
main()
