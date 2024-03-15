import configparser
import re
import glob
import os

# Initialize the configparser
config = configparser.ConfigParser()

# Read the properties.cfg file
config.read('properties.cfg')

# Retrieve the projectName and entrysymbol from the configuration file
projectName = config['DEFAULT']['projectName']
entrysymbol = config['DEFAULT']['entrysymbol']  # Retrieve entrysymbol

# Directory to check for .gdextension files
gdextension_dir = "{}/bin/".format(projectName)

# Search for .gdextension files in the specified directory
gdextension_files = glob.glob(gdextension_dir + "*.gdextension")

print(f"FIND ME: {gdextension_dir}")

# Check if there is at least one .gdextension file
if gdextension_files:
    # Use the first .gdextension file found (assuming there's only one)
    gdextension_file_path = gdextension_files[0]

    # Define the new file name based on projectName
    new_file_path = os.path.join(gdextension_dir, projectName + ".gdextension")

    # Rename the .gdextension file to match the projectName
    os.rename(gdextension_file_path, new_file_path)

    # Update the file path for further operations
    gdextension_file_path = new_file_path
    
    print(f"FIND ME 2: {gdextension_file_path}")
else:
    # If no .gdextension file is found, raise an error or handle accordingly
    raise FileNotFoundError("No .gdextension file found in " + gdextension_dir)

# Read the existing .gdextension file
with open(gdextension_file_path, "r") as file:
    file_contents = file.read()

# Update the entry_symbol in the .gdextension content
updated_contents = re.sub(r'entry_symbol = "[^"]+"', f'entry_symbol = "{entrysymbol}"', file_contents)

print(f"FIND ME 3 : {updated_contents}")

# Write the updated content back to the .gdextension file
with open(gdextension_file_path, "w") as file:
    file.write(updated_contents)
