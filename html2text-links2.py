#!/nix/store/pxh4mz0414n9gy7k2hl35i7shqh5jlx9-system-path/bin/python
import os
import subprocess

# Define your directories
input_folder = '/home/jq/prj/llamafile-rag/scrapes'  # Folder where HTML files are stored
output_folder = '/home/jq/prj/llamafile-rag/local_data'  # Folder where TXT files will be saved

# Function to check if the file contains HTML
def is_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(500)  # Read first 500 characters to check for HTML tags
            if '<html' in content.lower() or '<!doctype html' in content.lower():
                return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False

# Traverse the input folder
for root, dirs, files in os.walk(input_folder):
    for file in files:
        # Construct full file path for every file
        input_file = os.path.join(root, file)

        # Skip files that are not HTML
        if not is_html_file(input_file):
            print(f"Skipping non-HTML file: {input_file}")
            continue

        # Construct output folder path by mirroring the input folder structure
        relative_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, relative_path)

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Construct output file path (same name as the original file but with .txt extension)
        output_file = os.path.join(output_dir, file + '.txt')

        # Run `links -dump` and write the output to the text file
        try:
            with open(output_file, 'w') as f:
                subprocess.run(['links', '-dump', input_file], stdout=f)
            print(f"Processed: {input_file} -> {output_file}")
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")

