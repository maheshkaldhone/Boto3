import os
import re
import shutil

def is_valid_version(version):  
    return re.match(r'^\d+\.\d+\.\d+$', version)

def get_version_number(directory_name):
    # Extract the numeric version components and convert them to integers
    version_components = tuple(map(int, directory_name.split('.')))
    return version_components

def get_latest_version(directory_list):
    valid_versions = [version for version in directory_list if is_valid_version(version)]
    if not valid_versions:
        return None
    return max(valid_versions, key=get_version_number)

def main():
    source_directory = "/"  # Replace with the actual path of your directories
    destination_directory = "/path/to/destination"

    try:
        # Get a list of directories in the source directory
        directory_list = os.listdir(source_directory)

        if not directory_list:
            print("No directories found in the source directory.")
            return

        # Get the latest version directory
        latest_version_directory = get_latest_version(directory_list)

        if latest_version_directory is None:
            print("No latest version available.")
            return

        # Check if the latest version directory already exists in the destination
        destination_path = os.path.join(destination_directory, latest_version_directory)
        if os.path.exists(destination_path):
            print(f"No Latest version directory found. '{latest_version_directory}' already available in '/opt/artifactory'.")
        else:
            try:
                # Copy the latest version directory to the destination
                source_path = os.path.join(source_directory, latest_version_directory)
                shutil.copytree(source_path, destination_path)
                print(f"Latest version directory '{latest_version_directory}' copied to '/opt/artifactory' successfully.")
            except FileExistsError:
                print(f"Destination directory '{latest_version_directory}' already exists. Skipped copying.")
            except Exception as e:
                print(f"An error occurred while copying: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
