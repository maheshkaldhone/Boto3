#!/bin/bash

# Define the source and destination directories
SOURCE_DIR="/test"
DESTINATION_DIR="/opt/artifactory"

# Check if the source directory exists
if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Error: Source directory $SOURCE_DIR not found."
    exit 1
fi

# Get the latest update directory
latest_directory=""
latest_version="0.0.0"

for dir in "$SOURCE_DIR"/*/; do
    dir_name=$(basename "$dir")
    if [[ "$dir_name" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        if [[ "$dir_name" > "$latest_version" ]]; then
            latest_directory="$dir"
            latest_version="$dir_name"
        fi
    fi
done

# Check if a valid update directory was found
if [[ -z "$latest_directory" ]]; then
    echo "Error: No valid updated version found under $SOURCE_DIR."
    exit 1
fi

# Check if the latest directory already exists in the destination directory
if [[ -d "$DESTINATION_DIR/$latest_version" ]]; then
    echo "The latest version $latest_version is already available in $DESTINATION_DIR."
else
    # Copy the latest directory to the destination
    if cp -r "$latest_directory" "$DESTINATION_DIR"; then
        echo "Successfully copied the latest version $latest_version to $DESTINATION_DIR."
    else
        echo "Error: Failed to copy the latest version to $DESTINATION_DIR."
        exit 1
    fi
fi
