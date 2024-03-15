import argparse
import configparser
import subprocess
import sys
import os
import shutil

def check_or_install_package(package):
    """Check if a package is installed, and install it if it's not."""
    if not shutil.which(package):
        print(f"{package} is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print(f"{package} is already installed.")

def clone_godot_cpp(godot_version):
    """Clone the godot-cpp repository with the specified branch/version."""
    clone_command = [
        "git", "clone", "-b", godot_version, "https://github.com/godotengine/godot-cpp.git"
    ]
    print(f"Cloning godot-cpp with version: {godot_version}")
    subprocess.check_call(clone_command)
    os.chdir("godot-cpp")
    print("Initializing git submodules...")
    subprocess.check_call(["git", "submodule", "update", "--init"])
    os.chdir("..")

def run_scons_in_godot_cpp(thread_count):
    """Change to the godot-cpp directory, run scons with optional thread count."""
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.join(current_dir, "godot-cpp"))
        scons_command = ["scons"]
        if thread_count is not None:
            scons_command.append(f"-j{thread_count}")
        print("Running scons in godot-cpp...")
        subprocess.check_call(scons_command)
    finally:
        os.chdir(current_dir)

def create_godot_project(project_name):
    """Create a basic Godot project structure and project.godot file."""
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)
    project_file_path = os.path.join(project_dir, "project.godot")
    with open(project_file_path, 'w') as project_file:
        project_file.write(f"""[application]

name="{project_name}"
run/main_scene="res://main.tscn"

[editor]

project_settings/last_selected_path="res://"
""")
    print(f"Created Godot project '{project_name}' in {project_dir}")

def create_gdextension_file(project_name, config_path='properties.cfg'):
    """Create a .gdextension file with the entry symbol from properties.cfg."""
    config = configparser.ConfigParser()
    config.read(config_path)
    entry_symbol = config['DEFAULT'].get('entrysymbol', 'default_entry_symbol')

    gdextension_dir = os.path.join(os.getcwd(), project_name, "bin")
    os.makedirs(gdextension_dir, exist_ok=True)
    gdextension_file_path = os.path.join(gdextension_dir, f"{project_name}.gdextension")

    gdextension_contents = f"""[configuration]

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
"""
    with open(gdextension_file_path, 'w') as gdextension_file:
        gdextension_file.write(gdextension_contents)
    print(f"Created .gdextension file at {gdextension_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Setup script for initializing the Godot C++ bindings project.")
    parser.add_argument("-GodotVersion", type=str, required=True, help="Godot version to clone for godot-cpp")
    parser.add_argument("-ThreadCount", type=int, default=None, help="Number of CPU threads to use for scons")
    parser.add_argument("-ProjectName", type=str, required=True, help="Name of the Godot project to create")
    args = parser.parse_args()

    check_or_install_package("scons")
    create_godot_project(args.ProjectName)
    create_gdextension_file(args.ProjectName)
    clone_godot_cpp(args.GodotVersion)
    run_scons_in_godot_cpp(args.ThreadCount)

if __name__ == "__main__":
    main()
