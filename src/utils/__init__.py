from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import os
import boto3


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
    temp_filename = f"temp.{filetype}"
    with open(temp_filename, "w") as output:
        output.write(file_contents)

    return temp_filename


def get_csv_from_aws(path):
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket("service-outputs")

    local_file = "temp_rewards.csv"
    s3_bucket.download_file(path, local_file)

    return local_file
            