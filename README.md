# pyzipista
Tool to create a self-extracting Pythonista application

## Basic Functionality
The tool reads a configuration file and generates a Python script containing a zipped
base64 encoded data string of all files of a configured directory tree. Certain files
can be excluded using ignore files. The generated Python script will placed in the root 
directory of Pythonista as a "deployment file". Upon execution it will extract the encoded
directory tree as subtree relative to its own location.

## Prerequirements

You need to have Pythonista for iOS installed.

## Installation

The source code is available as a self-extracting Python script generated using the app on itself. See file `build/pyzipista_zip.py`. Download this file and follow the instructions contained therein.

Have fun!
