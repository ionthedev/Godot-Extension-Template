#!/usr/bin/env python
import configparser
import os
import glob

# Initialize the configparser
config = configparser.ConfigParser()

config.read('properties.cfg')

projectName = config['DEFAULT']['projectName']

env = SConscript("godot-cpp/SConstruct")

env.Append(CPPPATH=["src/"])
sources = glob.glob("src/*.cpp")

if env["platform"] == "macos":
    library = env.SharedLibrary(
        "{}/bin/{}.{}.{}.framework/gdexample.{}.{}".format(projectName, projectName,
            env["platform"], env["target"], env["platform"], env["target"]
        ),
        source=sources,
    )
else:
    # Corrected the path format here
    library = env.SharedLibrary(
        "{}/bin/{}{}{}".format(projectName, projectName, env["suffix"], env["SHLIBSUFFIX"]),
        source=sources,
    )

Default(library)
