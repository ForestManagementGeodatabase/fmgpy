# `fmgpy` PyCharm Configuration
This document describes how to set up your `fmgpy` development environment on 
your development computer. Since the `fmgpy` is tightly integrated with the 
ESRI Python APIs, we will be building off of an ESRI-provided conda environment 
to manage the packages installed for this project. 

## Clone the ESRI Conda Environment
In this step you'll use ESRI ArcGIS Pro to clone the ESRI-provided conda 
environment onto your computer to use for `fmgpy` development. 

* Cloned Conda Environment Path: 
* `C:\Users\<your_user>\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone`

## Clone the `fmgpy` Repository
In this step you'll use PyCharm to clone the `fmgpy` repository (repo) from the 
`MVR-GIS` GitHub organization onto your computer. 

## Configure PyCharm to Use Cloned Conda Environment
In this step you'll configure PyCharm to use the cloned ESRI conda environment 
for use by the `fmgpy` PyCharm project.  

Set Interpreter Paths:  
* Python Executable: `"C:\Users\B5PMMMPD\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\python.exe"`
* Conda Executable: `C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\conda.exe`

## Configure PyCharm to Use the ESRI Configured Command Prompts
In this step you'll configure PyCharm to use the ESRI-configured command prompt 
for managing this conda environment. 

* Terminal: `C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\proenv.bat`

