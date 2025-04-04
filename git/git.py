import datetime
import subprocess


class Git(object):
    def __init__(self, username: str, email: str, name: str, directory: str) -> None:
        self.username = username
        self.email = email
        self.name = name
        self.directory = directory

    def init(self):
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.directory,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to initialize Git repository: {e.output}") from e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while creating the repository: {str(e)}") from e

    def stage(self) -> None:
        try:
            subprocess.run(
                ["git", "stage", "."],
                cwd=self.directory,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to stage: {e.output}") from e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while staging: {str(e)}") from e

    def commit(self, at: datetime.datetime, message: str) -> None:
        try:
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", f"'{message}'"],
                cwd=self.directory,
                env={
                    "GIT_AUTHOR_NAME": self.username,
                    "GIT_AUTHOR_EMAIL": self.email,
                    "GIT_AUTHOR_DATE": at.isoformat(),
                    "GIT_COMMITTER_NAME": self.username,
                    "GIT_COMMITTER_EMAIL": self.email,
                    "GIT_COMMITTER_DATE": at.isoformat(),
                },
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to commit: {e.cmd}") from e
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while committing: {str(e)}") from e
