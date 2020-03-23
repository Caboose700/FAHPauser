# Folding@Home Pauser

> A simple Python script that will automatically pause and unpause Folding@Home if a specified application is running.

[![License](https://img.shields.io/github/license/Caboose700/FAHPauser)](http://badges.mit-license.org) ![Platform](https://img.shields.io/badge/python-v3.8.1-blue) ![Platform](https://img.shields.io/badge/platform-Windows-brightgreen)

## Configuration
On program start, the conf.json file is loaded. As an example, "notepad.exe" is present by default. For each application
you want Folding@Home to be paused when running, add the program's executable name into the JSON array and restart the program.

Make sure to use proper JSON syntax when adding programs to the array.
