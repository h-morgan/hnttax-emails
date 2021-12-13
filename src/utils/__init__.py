from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import os


def get_template_file_path(filename):
    """Open HTML file containing template for email to send"""
    dir_ = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(dir_)
    rel_path = f"templates/{filename}"
    abs_file_path = os.path.join(base_dir, rel_path)
    return abs_file_path


def generate_email_content(status, wallet, year, filetype):
    
    # build path to templates folder
    dir_ = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(dir_)
    rel_path = "templates/"
    template_path = os.path.join(base_dir, rel_path)

    # render the template
    env = Environment(
        loader = FileSystemLoader(template_path),
        trim_blocks=True,
        lstrip_blocks=True
    )

    template = env.get_template(f"{status}.{filetype}")

    file_contents = template.render(
        wallet = wallet,
        year = year
    )
    # save temp file 
    with open(f"temp.{filetype}", "w") as output:
        output.write(file_contents)

    return file_contents