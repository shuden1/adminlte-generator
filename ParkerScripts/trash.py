import os
import send2trash

def delete_html_folders(root_folder):
    for foldername, subfolders, filenames in os.walk(root_folder):
        if 'HTMLs' in subfolders:
            html_folder_path = os.path.join(foldername, 'HTMLs')
            print(f"Moving {html_folder_path} to trash.")
            send2trash.send2trash(html_folder_path)

if __name__ == "__main__":
    folder_to_search = input("Enter the path of the folder to search for HTMLs folders: ")
    delete_html_folders(folder_to_search)
    print("Operation completed.")
