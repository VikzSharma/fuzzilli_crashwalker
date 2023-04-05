import os
import subprocess
import argparse
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Define the path to the target binary
target_binary = "./jsc"

# Set up the command-line argument parser
parser = argparse.ArgumentParser(description='Run jsc tool on all .js files under a directory or subdirectory named crashes')
parser.add_argument('root_dir', metavar='root_dir', type=str, help='the root directory to search for crashes directory')
parser.add_argument('-v', '--verbose', action='store_true', help='display verbose output')
parser.add_argument('-o', '--output', type=str, help='save output in HTML format to the specified file')
parser.add_argument('-t', '--interval', type=int, default=60, help='time interval (in seconds) between each check for new files')
args = parser.parse_args()

# Initialize the output string and file counter
output_str = ""
file_count = 0

while True:
    # Loop through all the directories and subdirectories in the root directory
    for root, dirs, files in os.walk(args.root_dir):
        # Check if "crashes" directory is present in the current directory
        if "crashes" in dirs:
            # Get the path to the "crashes" directory
            crashes_dir = os.path.join(root, "crashes")

            # Loop through all the files in the "crashes" directory
            for file in os.listdir(crashes_dir):
                # Check if the file ends with .js and hasn't been processed before
                if file.endswith(".js") and file not in output_str:
                    # Increment the file counter
                    file_count += 1

                    # Create the command to run jsc with the file as an argument
                    file_path = os.path.join(crashes_dir, file)
                    command = [target_binary, file_path]

                    # Add the timestamp to the output string
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    output_str += f"<h1>{file} ({timestamp})</h1>\n"

                    if args.verbose:
                        print(f"Running target binary on file {file_path} ({timestamp}):")

                    try:
                        # Run the command and capture the output
                        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
                        output_str += f"<pre>{output.decode('utf-8')}</pre>\n"
                    except subprocess.CalledProcessError as e:
                        # Capture the exception and add it to the output string along with the command output
                        if args.verbose:
                            print(f"Error running target binary on file {file_path}: {e.output.decode('utf-8')}")
                        output_str += f"<pre>{e.output.decode('utf-8')}</pre>\n"

                    if args.verbose and not args.output:
                        print(output.decode("utf-8"))

    # Save the output as an HTML file
    if args.output:
        with open(args.output, "w") as f:
            f.write(str(BeautifulSoup(output_str, "html.parser")))

    # Print the number of files processed
    print(f"Processed {file_count} .js files.")

    # Wait for the specified interval before checking for new files again
    time.sleep(args.interval)
