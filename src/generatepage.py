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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with open(template_path) as template_file:
        template = template_file.read()
    # !!! Currently not creating new directory and putting a file in there
    # crawl every entry in the content directory
    filepaths = os.listdir(dir_path_content)
    # for each markdown file found, generate a new .html file using the template. Generated pages should end up in the public directory
    for filepath in filepaths:
        file_name = filepath.split("/")[-1]
        full_path = os.path.join(dir_path_content, filepath)
        if os.path.isdir(full_path):
            dest_path = os.path.join(dest_dir_path, filepath)
            os.mkdir(dest_path)
            generate_pages_recursive(full_path, template_path, dest_path)
        else:
            with open(full_path) as md_file:
                markdown = md_file.read()
            html = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

            write_path = os.path.join(dest_dir_path, filepath[0:-2] + "html")
            with open(write_path, "w") as new_file:
                new_file.write(html_page)

    
    







