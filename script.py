import os

def append_file_contents_to_txt(directory, output_file):
    """
    Browses a directory and all subdirectories, appends the contents of found files to a text file.

    Args:
        directory (str): The root directory to browse.
        output_file (str): The path to the output text file.
    """

    with open(output_file, "a", encoding="utf-8") as outfile:  # Open output file in append mode
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        outfile.write(f"File: {file_path}\n")
                        outfile.write(infile.read())
                        outfile.write("\n")  # Add a newline between files

                except UnicodeDecodeError:
                    print(f"Skipping binary file: {file_path}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")


if __name__ == "__main__":
    target_directory = "C:/Users/Ayoub/Desktop/PyDEGS-project/services"  # Replace with your directory
    output_txt_file = "output.txt"  # Replace with your desired output file name

    append_file_contents_to_txt(target_directory, output_txt_file)
    print(f"File contents appended to {output_txt_file}")