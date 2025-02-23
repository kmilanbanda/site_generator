import shutil
import  os
from generatepage import generate_page
from textnode import *

dir_path_static = "./static"
dir_path_public = "./public"
template_path ="./template.html"
filepath = "./content/index.md"
writepath = "./public/index.html"

def copy_static_to_public():
    print("Deleting public directory...")
    shutil.rmtree(dir_path_public)
    print("Copying static files to public directory...")
    shutil.copytree(dir_path_static, dir_path_public)

def main():
    copy_static_to_public()
    generate_page(filepath, template_path, writepath)

main()
