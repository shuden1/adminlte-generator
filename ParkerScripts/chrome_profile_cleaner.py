import os
import shutil
from pathlib import Path

def is_folder_in_use(folder_path):
    """Check if the folder is in use by attempting to rename it."""
    try:
        os.rename(folder_path, folder_path)
        return False
    except OSError:
        return True

def remove_unused_numeric_folders(directory):
    """Remove numeric folders that are not in use."""
    for folder in os.listdir(directory):
        folder_path = Path(directory) / folder
        if folder_path.is_dir() and folder.isdigit():
            if not is_folder_in_use(folder_path):
                shutil.rmtree(folder_path)
                print(f"Removed folder: {folder_path}")
            else:
                print(f"Folder in use, skipped: {folder_path}")

if __name__ == "__main__":
    directory = r"D:\Mind\CRA\AI_Experiments\Job_Crawlers\Peter\adminlte-generator\chrome_profile"
    remove_unused_numeric_folders(directory)
