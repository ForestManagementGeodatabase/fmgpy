# `fmgpy` PyCharm Configuration
This document describes how to set up your `fmgpy` development environment on your development computer. Since the `fmgpy` is tightly integrated with the ESRI Python APIs, we will be building off of an ESRI-provided conda environment to manage the packages installed for this project. The workflow specified here is based closely on the book [Python Packages](https://py-pkgs.org/), with adaptations for working within the ESRI Python ecosystem. 

## Clone the ESRI Conda Environment
In this step you'll use ArcGIS Pro to clone the ESRI-provided conda environment onto your computer to use for `fmgpy` development. 

* Cloned Conda Environment Path: 
* `C:\Users\<your_user>\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone`

## Clone the `fmgpy` Repository
In this step you'll use PyCharm to clone the `fmgpy` repository (repo) from the `MVR-GIS` GitHub organization onto your computer. 

## Configure PyCharm to Use Cloned Conda Environment from ESRI
In this step you'll configure PyCharm to use the cloned ESRI conda environment for use by the `fmgpy` PyCharm project.  

* File | Settings | Project | Python Interpreter | Show all | Add (+) 
* Add Python Interpreter | Conda Environment | Existing environment 
  * Interpreter: `"C:\Users\<your user>\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\python.exe"`
  * Conda Executable: `C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\conda.exe`
  * Make available to all projects: checked

## Configure PyCharm to Use the ESRI Configured Command Prompt
In this step you'll configure PyCharm to use the ESRI-configured command prompt (Windows: terminal or *nix: shell) for managing this conda environment [PyCharm Setup for ArcGIS Desktop](https://community.esri.com/t5/python-documents/pycharm-setup-for-arcgis-desktop/ta-p/1125129). 

File | Settings | Tools | Terminal | Applications Settings
* Shell Path: `C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\proenv.bat`

## Explore the Conda Environment
In this step you'll use the terminal command prompt to explore the Conda environment ([Reference](https://towardsdatascience.com/manage-your-python-virtual-environment-with-conda-a0d2934d5195)). In PyCharm, open a new terminal window and use the following conda commands. 

```shell
# Display a list of conda environments
# The active environment is marked with an *
conda env list

# Display details of the active environment
conda info

# Display a list of all installed packages
conda list

# Check conda configuration
conda config --show
```
See this [cheatsheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf) and the [conda user guide](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html) for more details.

## Install Python Packages
In this section you'll update the existing packages in the environment and install new packages. 

```shell
# Check for newer version of packages and install
conda update --all

# Install a specific package
conda install cookiecutter
```

Install from a specific conda channel:
```shell
# Install from a specific channel
conda install -channel esri arcpy
```

## Install the `poetry` Application
[`poetry`](https://python-poetry.org/docs/) is a tool for dependency management and packaging in Python. The current version of the `poetry` application must be manually installed using the [official installer](https://python-poetry.org/docs/master/#installing-with-the-official-installer). 

Windows Powershell:
```shell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | .\python -
```

Add the path to the `poetry.exe` file to your Windows user environment `PATH` variable: `C:\Users\B5PMMMPD\AppData\Roaming\Python\Scripts\poetry.exe` 


## Create a Virtual Environment for Package Development
In this step you'll create a virtual environment in which the `fmgpy` package will be developed ([see the docs for details](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment)). 

```shell
# Create a new conda virtual environment by cloning the base environment
conda create --name fmgpy-env --clone base

# Activate fmgpy-env
conda activate fmgpy-env

# Deactivate when finished
conda deactivate
```

## Initialize a preexisting project

```shell
cd c:\<path to your repo>\fmgpy

# Create a `project.toml` file
poetry init
```