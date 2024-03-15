import argparse
import configparser
import subprocess
import os
import shutil

def read_config(config_path='properties.cfg'):
    """Read values from properties.cfg."""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT'].get('projectName', ''), config['DEFAULT'].get('entrysymbol', 'default_entry_symbol')

def update_project_name_in_config(project_name, entry_symbol, config_path='properties.cfg'):
    """Update the projectName and entrysymbol in properties.cfg."""
    config = configparser.ConfigParser()
    config.read(config_path)
    if 'DEFAULT' not in config:
        config['DEFAULT'] = {}
    config['DEFAULT']['projectName'] = project_name
    config['DEFAULT']['entrysymbol'] = entry_symbol
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def clear_bin_directory(project_dir):
    """Clear all files inside the project's bin directory."""
    bin_dir = os.path.join(project_dir, 'bin')
    for filename in os.listdir(bin_dir):
        file_path = os.path.join(bin_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def update_gdextension_file(project_name, entry_symbol, project_dir):
    """Update the .gdextension file with the new project name and entry symbol."""
    clear_bin_directory(project_dir)  # Clear the bin directory first
    gdextension_dir = os.path.join(project_dir, 'bin')
    os.makedirs(gdextension_dir, exist_ok=True)
    gdextension_file_path = os.path.join(gdextension_dir, f'{project_name}.gdextension')

    with open(gdextension_file_path, 'w') as gdextension_file:
        gdextension_file.write(f"""[configuration]

entry_symbol = "{entry_symbol}"
compatibility_minimum = "4.2"
reloadable = true

[libraries]

macos.debug = "res://bin/{project_name}.macos.template_debug.framework"
macos.release = "res://bin/{project_name}.macos.template_release.framework"
windows.debug.x86_32 = "res://bin/{project_name}.windows.template_debug.x86_32.dll"
windows.release.x86_32 = "res://bin/{project_name}.windows.template_release.x86_32.dll"
windows.debug.x86_64 = "res://bin/{project_name}.windows.template_debug.x86_64.dll"
windows.release.x86_64 = "res://bin/{project_name}.windows.template_release.x86_64.dll"
linux.debug.x86_64 = "res://bin/{project_name}.linux.template_debug.x86_64.so"
linux.release.x86_64 = "res://bin/{project_name}.linux.template_release.x86_64.so"
linux.debug.arm64 = "res://bin/{project_name}.linux.template_debug.arm64.so"
linux.release.arm64 = "res://bin/{project_name}.linux.template_release.arm64.so"
linux.debug.rv64 = "res://bin/{project_name}.linux.template_debug.rv64.so"
linux.release.rv64 = "res://bin/{project_name}.linux.template_release.rv64.so"
android.debug.x86_64 = "res://bin/{project_name}.android.template_debug.x86_64.so"
android.release.x86_64 = "res://bin/{project_name}.android.template_release.x86_64.so"
android.debug.arm64 = "res://bin/{project_name}.android.template_debug.arm64.so"
android.release.arm64 = "res://bin/{project_name}.android.template_release.arm64.so"
""")
    print(f"Updated .gdextension file at {gdextension_file_path}")

def update_project_directory_and_file(project_name_old, project_name_new, entry_symbol):
    """Rename the project directory and update project.godot and .gdextension files."""
    project_root_dir = os.getcwd()
    project_dir_old = os.path.join(project_root_dir, project_name_old)
    project_dir_new = os.path.join(project_root_dir, project_name_new)

    if os.path.isdir(project_dir_old) and project_name_old != project_name_new:
        os.rename(project_dir_old, project_dir_new)
        project_file_path = os.path.join(project_dir_new, "project.godot")
        if os.path.exists(project_file_path):
            with open(project_file_path, 'r') as file:
                filedata = file.read()
            filedata = filedata.replace(f'name="{project_name_old}"', f'name="{project_name_new}"')
            with open(project_file_path, 'w') as file:
                file.write(filedata)

        update_gdextension_file(project_name_new, entry_symbol, project_dir_new)
        print(f"Project directory and files updated to '{project_name_new}'.")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Build script for updating project name, running scons, and cleaning up afterwards.")
    parser.add_argument("-ThreadCount", type=int, help="Number of CPU threads to use", default=None)
    parser.add_argument("-ProjectName", type=str, help="Project name to update in properties.cfg and rename project directory", default=None)
    args = parser.parse_args()

    old_project_name, entry_symbol = read_config()

    # Update the project name in properties.cfg and project directory if -ProjectName is provided
    if args.ProjectName:
        print(f"Updating project name to '{args.ProjectName}' and entrysymbol to '{entry_symbol}' in properties.cfg...")
        update_project_name_in_config(args.ProjectName, entry_symbol)
        update_project_directory_and_file(old_project_name, args.ProjectName, entry_symbol)

    # Construct and run the scons command
    scons_command = ["scons"] + (["-j", str(args.ThreadCount)] if args.ThreadCount is not None else [])
    print("Running scons...")
    subprocess.run(scons_command)

    # After scons completes, optionally run CleanGDExtension.py or any other cleanup script
    print("Running CleanGDExtension.py...")
    subprocess.run(["python", "CleanGDExtension.py"])

if __name__ == "__main__":
    main()
