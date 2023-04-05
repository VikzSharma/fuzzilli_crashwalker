**Description**

Quick dirty python script that recursively searches for all .js files in a given Fuzzilli fuzzer output directory (including subdirectories ( Master , Slaves etc.), runs them through the target binary, and saves the output of each execution in an HTML file. Additionally, the script prints out the number of .js files executed and the timestamp for each execution. It also monitors the directory continuously and update the HTML file with new results as they come in.

**Usage**
To use this script, follow these steps:

1. Update `target_binary` in the script with the target binary location.
2. Clone this repository or download the crashwalker.py file.
3. To run the script once on a specific directory, use the following command:

`python crashwalker.py -o <path_to_html_file>  <path_to_fuzzer_output> -v`

Replace **<path_to_fuzzer_output>** with the path to the output directory of fuzzer to search for .js files in, and **<path_to_html_file>** with the path to the HTML report file where you want to save the output.

This will run the script once and then continue to monitor the directory for changes. If any .js files are added or modified, the script will automatically run given target binary on them and update the HTML file with the new output.

**Note:** The script will continue to run until it is manually stopped (e.g., by pressing Ctrl + C in the terminal window).

**References :**

https://github.com/googleprojectzero/fuzzilli
