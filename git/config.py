import subprocess


def get_user_name() -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "user.name"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to get user name from Git configuration.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while getting the user name: {str(e)}") from e


def get_user_email() -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "user.email"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to get user email from Git configuration.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while getting the user email: {str(e)}") from e
