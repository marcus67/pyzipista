![gitsynchista icon](https://raw.githubusercontent.com/marcus67/pyzipista/master/lib/pyzipista_64x64.png)

# pyzipista
Tool to create a self-extracting Pythonista application.

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

## Configuration
Each application for which a self-extracting archive shall be created needs to have a `pyzipista_config` configuration file. As a convention this file should be placed in the `etc` subdirectory of the application directory. A sample configuration file can be found [here](https://raw.githubusercontent.com/marcus67/pyzipista/master/etc/pyzipista_config_sample).

Once the configuration has been created the most convenbient way to call pyzipista is to create an action shortcut in Pythonista using the filename of the configuration file as the first and only parameter. It is advisable to use a relative path with respect to the location of the `pyzipista.py` script.

## Support in gitsynchista

The synchronization app [gitsynchista](https://github.com/marcus67/gitsynchista) has automatic support for pyzipista if a pyzipista configuration file is found in the main or the `etc` subdirectory of a repository. In this case pyzipista can be called by pressing a button of the gitsynchista GUI. For more details see the [Readme](https://github.com/marcus67/gitsynchista/blob/master/README.md). 

## Feedback and Questions

For feedback (bug reports) [open an issue at GitHub](https://github.com/marcus67/pyzipista/issues/new). If you have questions about the tool see the [Pythonista Forum](https://forum.omz-software.com/category/5/pythonista).


Have fun!
