# qMODES (A Global Moisture Decomposition Software Package)

## UPDATE WARNING

**IMPORTANT NOTE!!! MUCH OF THE INFO IN THIS README FILE IS INCORRECT, AS MAJOR UPDATES ARE CURRENTLY UNDERWAY. THIS README WILL BE FULLY UPDATED SOON ONCE THE CHANGES HAVE BEEN COMPLETED.**


## DESCRIPTION

This package is used to compute Inertio Gravity (EIG/WIG), Rossby (ROT), and Moisture (M) modes, as outlined in the 2026 paper [Moisture Decomposition With Normal Modes in Global Data: Balanced and Unbalanced Components](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JD045439) by Kumm, Stechmann, Zagar, and Neduhal. This package was developed in support of the work performed in said paper, and includes the Python package and scripts necessary to compute both the physical space and Fourier space q components outlined therein as well as some of the scripts used to analyze and plot the data.
    
If you are not looking to modify the code at all it is recommended to use the docker image associated with this repository. 


## qMODES Package Structure

Default / recommended directory structure when using the qMODES model/repository to run the qMODES code. In this diagram the default "demo run" (present in the base repository) and a "new run" (run_A) are shown as examples. Note the virtual environment directory "qMODES_venv" is not included here as it is not directly 

```
|-- qMODES_repository/
|   | 
|   |-- .github/
|   |-- .gitignore
|   |-- Dockerfile
|   |-- LICENSE.md
|   |-- README.md
|   |-- qMODES_requirements.txt
|   |
|   |-- data
|   |   |-- input_data/   [SL]
|   |   |-- output_data/  [SL]
|   |
|   |-- runs/
|   |   |
|   |   |-- run_demo/
|   |   |   |-- config_demo.yaml
|   |   |   |-- submit_job_demo.sh
|   |   |   |-- input_data_demo/   [SL]
|   |   |   |-- output_data_demo/  [SL]
|   |   |  
|   |   |-- run_A/
|   |   |   |-- config_A.yaml
|   |   |   |-- submit_job_A.sh
|   |   |   |-- input_data_A/   [SL]
|   |   |   |-- output_data_A/  [SL]
|   |
|   |-- plots
|   |   |-- plots_demo/
|   |   |-- plots_A/
|   |
|   |-- src/qMODES/
|   |   |--__init__.py
|   |   |-- other_qMODES_package_scripts.py
|   |
|   |-- tests/
|   |   |-- test_config.yaml
|   |   |-- test_data_manager.py
|   |   |-- test_data
|   |   |   |-- test_input_data
|   |   |   |-- test_output_data
|   |
|   |-- notebooks/

*[SL] = recommended to make a symbolic link to a large storage area (scratch space)

```

Recommended Directory structure for Large Storage Space

```
|-- qMODES_data/
|   |
|   |-- input_data/
|   |   |-- ERA_data/
|   |   |-- MODES_data/
|   |   |   |-- coef
|   |   |   |-- hough
|   |   |   |-- vsf
|   |
|   |-- output_data
|   |   |-- experiment_A_output_data
|   |   |   |-- qk_data
|   |   |   |-- qmodes_data
|   |   |
|   |   |-- experiment_B_output_data
|   |   |   |-- qk_data
|   |   |   |-- qmodes_data
```

## Using the Docker Image

Stuff describing how to use the Docker Image and a link to it's location in Docker Hub. 

## Initial Setup For non-Docker Image version

0) Make sure python is installed on your machine

1) Download the codebase, probably through the github repo (link)

2) setup a python venv for qMODES (qMODES_venv) in repo base dir.

3) install python packages using pip and qMODES_requirements.txt file

4) modify setup_qMODES.sh file (PYTHONPATH, ENVVARS, etc...)

5) Add QMODES_BASE_DIR environment variable to your startup file (.bash_profile, .bashrc, .zshrc, etc...) to automatically run the setup_qMODES.sh file and optionally add lines to run setup_qMODES.sh on startup if you will be consistently using this.

5) run tests to make sure everything works (test_data_manager to generate data, )




<!-- COMMENT OUT
## UPDATE WARNING

**IMPORTANT NOTE!!! MUCH OF THE INFO IN THIS README FILE IS INCORRECT, AS MAJOR UPDATES ARE CURRENTLY UNDERWAY. THIS README WILL BE FULLY UPDATED SOON ONCE THE CHANGES HAVE BEEN COMPLETED.**

## DESCRIPTION 

This package is used to compute Inertio Gravity (EIG/WIG), Rossby (ROT), and Moisture (M) modes, as outlined in the 2026 paper [Moisture Decomposition With Normal Modes in Global Data: Balanced and Unbalanced Components](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2025JD045439) by Kumm, Stechmann, Zagar, and Neduhal. This package was developed in support of the work performed in said paper, and includes the Python package and scripts necessary to compute both the physical space and Fourier space q components outlined therein as well as some of the scripts used to analyze and plot the data.
    
If you are not looking to modify the code at all it is recommended to use the docker image associated with this repository. 

DIRECTIONS FOR USING THE DOCKER IMAGE WILL SOON BE ADDED TO THIS README.

This software package is designed to take ERA5 global reanalysis data and modal decomposition data from the MODES software package (developed by the Zagar group at the University of Hamburg) as inputs in order to perform the computations. For more information on these see the following links to the [CDS ERA5 dataset](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-complete?tab=overview) and [MODES software](https://modes.cen.uni-hamburg.de/). 

Contained in this repository are the scripts necessary to perform the main qMODES computations as well as several scripts that may be useful for data analysis and visualization. There are also several other sample scripts that may be useful in aquiring the necessary input data.

## DOCKER IMAGES 

It is recommended to use the qMODES Docker image if you are not planning on making any major changes to the code.

The qmodes docker images can be found [here](https://hub.docker.com/repository/docker/brkumm92/qmodes/):

The qmodes image is setup to import everything in the GitHub repo. Note that the GitHub repo doesn't contain any of the input data necessary to run the code. Therefore the code should be run by mounting two volumes when running a qmodes container. The default directory structure setup in the Docker image is assumed to be.

    
```
|-- /qMODES
|    |
|    |-- /calculation_scripts
|    |    |- ... 
|    |
|    |-- /misc
|    |    |- ... 
|    |
|    |-- /src
|    |    | - /qMODES
|    |         |- ...
|    |
|    |-- /tests
|    |    |- ...
|    |
|    |- ...
|
|-- /input_data
|    |
|    |- /ERA_data
|    |   |- ...
|    |
|    |- /MODES_data
|    |   |- /coef
|    |   |   |- ...
|    |   |
|    |   |- /hough
|    |   |   |- ...
|    |   |
|    |   |- /vsf
|    |   |   |- ...
|       
|-- /output_data
|    |
|    |-- /plots
|    |    |- ...
|    |
|    |-- /qk_data
|    |    |- ...
|    |
|    |-- /qmodes_data
|    |    |- ...
```

Note: The file structure can be changed if you would like to, however you will also need to change the file structure environment variables as the qMODES Python package is to read in these variables throughout the code.


## DEPENDENCIES
    
This software package is largely written in python, and as such it is recommended to use a python virtual environment (pyvenv) to handle all of the dependencies for running the qMODES software. A pyvenv requirements file titled "pyvenv_qMODES_requirements.txt" has been included in the base directory which describes the dependencies of the qMODES software package.

An additional requirements.txt file is also included which contains the dependencies for running the 


## qMODES SOFTWARE DIRECTORY OVERVIEW 

The directory system for the qMODES software package immediately after installation is as follows:

```
qMODES
 |-- docs
 |-- input_data
 |    |-- ERA_data
 |    |-- MODES_data
 |         |-- coef
 |         |-- hough
 |         |-- vsf
 |         |-- vsf_int
 |
 |-- output_data
 |    |-- plots
 |    |-- qk_data
 |    |-- qMODES_data
 |
 |-- src
 |    |-- plotting_scripts
 |    |-- qMODES_scripts
 |    |-- misc
 |
 |-- tests
 ```

A breif description of each of the directories is as follows:

> docs: Directory for the user to record any desired documentation.
> input_data: General directory to store all input data.
> ERA_data: Directory to store ERA input data.
> MODES_data: Directory to store MODES input data.
> coef: Directory to store the MODES coefficients.
> hough: Directory to store the MODE hough (and frequency) data.
> vsf: Directory to store the MODES vsf function data.
> vsf_int: Directory to store the integrated vsf data.
> output_data: General directory to store all output data.
> plots: Directory to store plots and other data visulizations.
> qk_data: Directory to store Fourier space output data.
> qMODES_data: Directory to store physical space output data.
> src: General directory for the main scripts
> plotting_scripts: Directory for plotting scripts
> qMODES_scripts: Directory for main computation scripts
> misc: Directory for other miscellaneous scripts
> tests: Directory for testing scripts


## RETRIEVING INPUT DATA 

As mentioned above ERA5 global reanalysis data and global decompostiion data from the MODES software package will need to be aquired to perform the main decomposition computations.

#### ERA Data
To obtain ERA5 global reanalysis data you will have to create an account with ECMWF. After doing so it is recommended to use an API to retrieve the data.

A sample API script is located in src/misc which will
likely need to be modified to aquire the exact data you wish to
analyze. The data that this script downloads should be placed in
the input_data/ERA_data/ directory.

Currently the software is set up to only run the first timestep saved in any given ERA data file AND the ERA data files are expected to be in netCDF (*.nc) format. Therefore, for each timestep you would like to generate data for YOU NEED TO save the data for that timestep in it's own netCDF file.
    
#### MODES Data
If you would like to aquire the data that was used in the paper mentioned above the zenodo links are given below:

> <https://doi.org/10.5281/zenodo.12726172>\
> <https://doi.org/10.5281/zenodo.12724196>\
> <https://doi.org/10.5281/zenodo.12749244>\
> <https://doi.org/10.5281/zenodo.12749316>\
> <https://doi.org/10.5281/zenodo.12749407>\
> <https://doi.org/10.5281/zenodo.12749482>\
> <https://doi.org/10.5281/zenodo.12751158>\
> <https://doi.org/10.5281/zenodo.12751242>\
> <https://doi.org/10.5281/zenodo.12751345>\
> <https://doi.org/10.5281/zenodo.12751416>\

To aquire additional MODES modal decomposition data you should contact the Zagar group at the University of Hamburg who created and maintains the MODES software package. The data you will need to acquire from them includes the vertical structure functions (VSF's), Hough functions and their associated frequencies, and the Hough coefficients. These data should then be stored in the following qMODES directories:

> vertical structure functions (VSFs)-> input_data/MODES_data/vsf/ \
> Hough functions and frequencies    -> input_data/MODES_data/hough/ \
> Hough coefficients                 -> input_data/MODES_data/coef/ \

NOTE: The hough function files and frequency files should BOTH be
stored in the input_data/MODES_data/hough/ directory.

## RUNNING THE SOFTWARE

THIS SECTION WILL BE UPDATED SOON TO INCLUDE RUNNING THE CODE AS A DOCKER CONTAINER.

Currently the qMODES software is configured so that a single run produces values for a the first timestep of an single ERA5 data file and it corresponding MODES decomposition data. A big picture list of steps for how to perform a single run is as follows.

> -1. Make sure the ERA5 and MODES input data is downloaded as 
>     described above.
> 
> 0.  Precompute the integrated vertical structure functions (VSF's) 
>     using the /src/qMODES_scripts/Calculate_Integrated_VSFs.py 
>     script and store them in the input_data/MODES_data/vsf_int/ 
>     directory. Precomputing (and storing) these values allows this
>     step to be skipped for future runs which use the same VSF's.
> 
> 1.  Compute the Fourier space (qk) values by running the script 
>     /src/qMODES_scripts/Calculate_qk.py and store the results in
>     /output_data/qk_data/. 
>        
>     When running the script in the command line you will need to 
>     specify the '-d' and '-m' flags/parameters which are flags for 
>     the date (in YYYYMMDD format) and MODE (EIG, WIG, or BAL) for 
>     the given run. The script will attempt tosave data for each of 
>     the different modes (EIG, WIG, or BAL) in the same file, as 
>     long as a file for that date already exists.
> 
> 2.  Compute the physical space values (qMODES) by running the script
>     /src/qMODES_scripts/Calculate_qMODES.py and store the results in
>     /output_data/qMODES_data/

At the moment the physical space and fourier space grid parameters are hard coded into each of the scripts where they are relevant. Hopefully this will be fixed with an update soon.


## VERSION HISTORY COMMENTS 

The current version is the initial commit. Comments on different versions may appear here in later versions.


## LISCENSE     

The liscense for the qMODES software package is a standard Creative Commons 1.0 Liscense. For more information see the file titled LISCENSE.md in the base directory.


## CONTRIBUTORS 

Bradley Kumm, PhD \
University of Wisconsin - Madison \
bkumm at wisc dot edu or brkumm at gmail dot com 

Valentino Neduhal \
University of Hamburg \
valentino dot neduhal at uni-hamburg dot de 

Sam Stechmann, PhD \
University of Wisconsin - Madison \
stechmann at wisc dot edu 

Nedjeljka Zagar, PhD \
University of Hamburg \
nedjeljka dot zagar at uni-hamburg dot de 

## ACKNOWLEDGEMENTS 

Zagar Group and specifically, Nedjeljka Zagar and Valentino Neduhal for all of their help producing obtaining and understanding the MODES software data which served as input to our qMODES package, and help with understanding this data, and also for their feedback and insights during this research project.

ECMWF for producing and distributing the ERA5 reanalysis data sets.
END COMMENT OUT -->