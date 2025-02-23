from blockmarkdown import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            title = line.strip("#").strip()
            break
    if title == "":
        raise Exception("No valid header was found")
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    
    # open and read files
    with open(from_path) as md_file:
        markdown = md_file.read()
    
    with open(template_path) as template_file:
        template = template_file.read()

    # fill template
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # write HTML page
    with open(dest_path, "w") as new_file:
        new_file.write(html_page)
    
    







