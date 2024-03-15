# Godot-Extension-Template
Making the development of Godot Extensions easier for everyone.

After following the GDExtension example from the Godot Documentation, I realized this is an extremely cumbersome process to work within, so I wanted to attempt to make it easier, feel free to make a pull request if you have some changes you'd like implemented. This project contains C++ files, directly using the code from Godot's Documentation. https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/gdextension_cpp_example.html

## DISCLAIMER
This current build does not contain godot-cpp, it will actively install it for you. 

## Prerequisites
Git and Git Bash
A Godot 4 Executable
Visual Studio Build Tools
VSCode with C/C++ Extension.
A C++ Compiler, I am using MingW https://www.mingw-w64.org/
Python


## Setup
Once you have these things installed, open the repo in VS Code and open a new Terminal in VS Code.

run the setup.py script. This script has 2 neccessary argument called "-GodotVersion" and "-ProjectName", it also hasan optional one called "-ThreadCount".

If you want to target Godot 4.1 with no set threadcount, that would look like
"python setup.py -GodotVersion 4.1 -ProjectName ExampleProject"

If you want to target Godot 4.2 with threads, replace _x_ with however many threads you want.
"python setup.py -GodotVersion 4.2 -ProjectName ExampleProject -ThreadCount _x_"

This will clone the Godot-CPP repo for you and select the version you specified. After it gets Godot-CPP, it will then run Scons to build the binary for the Godot-CPP static libraries. A godot project will also be automatically generated with your project name

Once this is done, you should be all begin building your plugin.

## Building your Plugin
While you can follow the godot documentation for this step, you can also run my custom "build.py" file.
build.py has 1 neccessary argument called -ProjectName and an optional one called -ThreadCount.

before building your plugin, make sure in the properties.cfg file, the "entrysymbol" section has the exact name as the "GDExtensionBool GDE_EXPORT" at the bottom of your register_types.cpp file

To build your plugin, run the following command in terminal. 12 threads, replace _x_ with however many threads you want.

"python build.py -ThreadCount _x_ -ProjectName Example"

