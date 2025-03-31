import datetime
import os

from jinja2 import Environment, FileSystemLoader

from git.git import Git


def create_repo(git: Git, name: str, directory: str, at: datetime.datetime) -> None:
    """
    Create a new Git repository in the specified working directory.

    :param git: An instance of the Git class to interact with the Git system.
    :param name: The name of the new repository.
    :param directory: The directory where the repository will be created.
    """

    # Check if the directory already exists
    if os.path.exists(directory):
        print(f"Directory {directory} already exists. Please choose a different name.")
        return

    # Create the new directory
    os.makedirs(directory)

    # Initialize a new Git repository
    git.init()

    # Start up the templating system
    env = Environment(loader=FileSystemLoader("templates"))

    # Walk through the templates directory
    for root, _, files in os.walk("templates"):
        for file in files:
            template_path = os.path.join(root, file)
            relative_path = os.path.relpath(template_path, "templates")
            output_path = os.path.join(directory, relative_path)

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Render the template and write to the output file
            template = env.get_template(relative_path)
            rendered = template.render(
                repo_name=name,
                generated_on=datetime.date.today().isoformat(),
            )

            with open(output_path, "w") as f:
                f.write(rendered + "\n")

    # Make the initial commit
    git.stage()
    git.commit(at, "feat: Initial commit")
