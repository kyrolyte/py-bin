# Py Bin

This repository contains a collection of miscellaneous Python scripts and small program files to help improve and automate various tasks or to experiment. It also includes commands and instructions for different setups such as local utilities, data processing helpers, and project-support functions.

## Purpose

The intention of this repository is to be used as a reference guide for a variety of tasks implemented in Python. These tasks can range from automation and file handling to data formatting, simple tooling, or setting up configurations within a project or server environment. This repository serves as a single centralized place to reference these scripts and small programs for future use. Some scripts were used for niche purposes on various projects, and others (but not all) are also copied over to GitHub Gists.

In particular, some of these scripts are context-agnostic versions of tools originally written for major projects, especially those that process or format files. The goal is to preserve reusable patterns and logic without tying them to any one codebase.

## Usage

Most scripts in this repository are designed to be run as standalone Python programs. Typical usage patterns include:

- Running a script directly from the command line, for example:
  - `python path/to/script.py`
  - `python -m module_name` when organized as a module
- Passing input files, directories, or flags via command-line arguments.
- Importing a script as a module in another project to reuse functions or classes.

Each script should include either:
- A short comment at the top describing its purpose, or
- A `--help` option via `argparse` (or similar) to outline available arguments and expected inputs.

Refer to individual script docstrings or help output for details on required arguments and expected behavior.

## Python version and dependencies

Unless otherwise noted, scripts are intended to run on a recent version of Python 3 (for example, Python 3.10 or later). Some scripts rely only on the standard library, while others use external packages.

Where external dependencies are required, they are listed in a `requirements.txt` file or in comments at the top of the script. It is recommended to install and run these dependencies inside a virtual environment rather than globally.

## Setting up a virtual environment

To keep dependencies isolated and avoid conflicts with global Python packages, it is recommended to create and activate a virtual environment before installing any required libraries.

### 1. Create a virtual environment

From the root of this repository, run:

- On most systems:
  - `python -m venv .venv`

If your system uses `python3` as the executable name:

- `python3 -m venv .venv`

This creates a `.venv` directory containing an isolated Python environment.

### 2. Activate the virtual environment

- On macOS and Linux:
  - `source .venv/bin/activate`
- On Windows (PowerShell):
  - `.venv\Scripts\Activate.ps1`
- On Windows (Command Prompt):
  - `.venv\Scripts\activate.bat`

Once activated, your shell prompt should indicate that the virtual environment is active, and `python` / `pip` will refer to the environment’s interpreter and packages.

### 3. Install dependencies

If a `requirements.txt` file is present, install all required packages with:

- `pip install -r requirements.txt`

Some scripts may instead list their dependencies in comments or separate files. In those cases:

- Review the script or accompanying notes for the required packages.
- Install them with `pip install package_name`.

Repeat this process whenever new scripts are added that require additional third-party libraries.

### 4. Deactivate the virtual environment

When finished, you can deactivate the virtual environment with:

- `deactivate`

This returns the shell to using the system’s default Python interpreter and environment.

## Disclaimer

Please note that the scripts provided in this repository are meant to be used at the discretion of the user. While they have been created with care, it is important to understand that they might need adjustments to work in your specific environment, Python version, or scenario.

In addition, you are responsible for reviewing and understanding the scripts before running them on your system. Always test scripts on non-critical data first and ensure they behave as expected in your environment.
