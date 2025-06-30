from pathlib import Path

# Get the current working directory as a Path object
current_directory = Path.cwd()

print(f"The current working directory is: {current_directory}")

# Get the user's home directory
home_directory = Path.home()

print(f"The user's home directory is: {home_directory}")