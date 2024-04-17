import os

# Get the user's home directory
home_directory = os.path.expanduser("~")

# Define the output file path
output_file = os.path.join(home_directory, "Documents", "drivescan_results.txt")

# Define the command to search for files over 1GB and in the trash bin directories
combined_command = f"find /home -mtime +30 -daystart > {output_file} && sudo find / -xdev -type f -size +1G > {output_file} && sudo find /home/*/.local/share/Trash -type f >> {output_file}"

# Execute the combined command
os.system(combined_command)

print("Scan results saved to:", output_file)

