import os
import shutil

def move_folders_without_htmls(source_folder):
    # Define the path to the Archive folder within the source folder
    archive_folder = os.path.join(source_folder, 'Archive')

    # Create the Archive folder if it does not exist
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Iterate through each item in the source folder
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        # Check if the current item is a folder (excluding the Archive folder itself)
        if os.path.isdir(item_path) and item != 'Archive':
            # Check if the folder contains a subfolder named 'HTMLs'
            if not any(os.path.isdir(os.path.join(item_path, name)) and name == 'HTMLs' for name in os.listdir(item_path)):
                # Move the folder to the Archive folder
                destination_path = os.path.join(archive_folder, item)
                print(f"Moving '{item_path}' to '{destination_path}'")
                shutil.move(item_path, destination_path)

# Set the initial folder path here
source_folder = 'D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\Companies'
move_folders_without_htmls(source_folder)
