from datetime import date
import os
import subprocess

from jinja2 import Environment, FileSystemLoader

def create_repo(repo_name: str, repo_directory: str) -> None:
    """
    Create a new Git repository in the specified working directory.
    
    :param name: The name of the new repository.
    :param repo_directory: The directory where the repository will be created.
    """
    
    # Check if the directory already exists
    if os.path.exists(repo_directory):
        print(f"Directory {repo_directory} already exists. Please choose a different name.")
        return
    
    # Create the new directory
    os.makedirs(repo_directory)
    
    # Initialize a new Git repository
    subprocess.run(["git", "init"], cwd=repo_directory)
    
    print(f"Created new Git repository at {repo_directory}")

    # Start up the templating system
    env = Environment(loader=FileSystemLoader("templates"))


    # Add a README file
    readme_path = os.path.join(repo_directory, "README.md")
    template = env.get_template("README.md")
    rendered = template.render(
        repo_name=repo_name,
        generated_on=date.today().isoformat()
    )

    with open(readme_path, "w") as f:
        f.write(rendered + "\n")
    