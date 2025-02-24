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
    # open, read, and close template file
    with open(template_path) as template_file:
        template = template_file.read()

    # get filepaths
    filepaths = os.listdir(dir_path_content)

    # iterate through all filepaths
    for filepath in filepaths:
        # get the full "from" path (from my content)
        from_path = os.path.join(dir_path_content, filepath)

        # determine if the path points to a file or directory
        if os.path.isdir(from_path):
            # create the directory in public at dest_path
            dest_path = os.path.join(dest_dir_path, filepath)
            os.mkdir(dest_path)

            # recursively call for the files within from_path to be generated and written to the public directory
            generate_pages_recursive(from_path, template_path, dest_path)
        else:
            # open, read, and close the file
            with open(from_path) as md_file:
                markdown = md_file.read()
            
            # convert the markdown to html, extract the title, and create the html page from the template
            html = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

            # write the html page
            write_path = os.path.join(dest_dir_path, filepath[0:-2] + "html")
            with open(write_path, "w") as new_file:
                new_file.write(html_page)

    
    







