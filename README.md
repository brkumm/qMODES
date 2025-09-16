qMODES (A Global Moisture Decomposition Software Package)

----------------------------- DESCRIPTION -----------------------------

    This software package is used to compute the Easterly/Westerly 
    Inertio Gravity (EIG/WIG), Rossby (ROT), and Moisture (M) modes, as
    outlined in the 2025 paper (currently submitted to JGR Atmospheres)
    titled "Moisture decomposition with normal modes in global data: 
    balanced and unbalanced components" by Kumm, Stechmann, Zagar, and
    Neduhal. This package was developed in support of the work 
    performed in said paper, and includes the scripts necessary to 
    compute both the physical space and Fourier space q components 
    outlined therein.

    This software package is designed to take ERA5 global reanalysis 
    data and modal decomposition data from the MODES software package 
    (developed by the Zagar group at the University of Hamburg) as 
    inputs in order to perform the computation. For more information on 
    these data see https://cds.climate.copernicus.eu/datasets/reanalysis-era5-complete?tab=overview 
    and here https://modes.cen.uni-hamburg.de/ . Or see the paper for
    references to the zenodo links for these data.

    Contained in this package are the scripts necessary to perform the 
    main qMODES computations as well as several scripts that may be 
    useful for data analysis and visualization. There are also several
    other sample scripts that may be useful in aquiring the necessary 
    input data.

    Several aspects of this package may be updated in the future.
    To check if there is an updated version of the qMODES software check
    the GitHub repository https://github.com/brkumm/qMODES/ .


----------------------------- DEPENDENCIES ----------------------------

    This software package is largely written in python, and as such it 
    is recommended to use a python virtual environment (pyvenv) to 
    handle all of the dependencies for running the qMODES software. A 
    pyvenv requirements file titled "pyvenv_qMODES_requirements.txt" 
    has been included in the base directory which describes the 
    dependencies of the qMODES software package.

    An additional requirements.txt file is also included which contains 
    the dependencies for running the 


------------------ qMODES SOFTWARE DIRECTORY OVERVIEW -----------------

    The directory system for the qMODES software package immediately 
    after installation is as follows:

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

     A breif description of each of the directories is as follows:

     docs: Directory for the user to record any desired documentation.
     input_data: General directory to store all input data.
     ERA_data: Directory to store ERA input data.
     MODES_data: Directory to store MODES input data.
     coef: Directory to store the MODES coefficients.
     hough: Directory to store the MODE hough (and frequency) data.
     vsf: Directory to store the MODES vsf function data.
     vsf_int: Directory to store the integrated vsf data.
     output_data: General directory to store all output data.
     plots: Directory to store plots and other data visulizations.
     qk_data: Directory to store Fourier space output data.
     qMODES_data: Directory to store physical space output data.
     src: General directory for the main scripts
     plotting_scripts: Directory for plotting scripts
     qMODES_scripts: Directory for main computation scripts
     misc: Directory for other miscellaneous scripts
     tests: Directory for testing scripts


----------------------- RETRIEVING INPUT DATA ------------------------

    As mentioned above ERA5 global reanalysis data and global 
    decompostiion data from the MODES software package will need to be
    aquired to perform the main decomposition computations.

    ---------- ERA Data ----------
    To obtain ERA5 global reanalysis data you will have to create an 
    account with ECMWF. After doing so it is recommended to use an API
    to retrieve the data.

    A sample API script is located in src/misc which will 
    likely need to be modified to aquire the exact data you wish to 
    analyze. The data that this script downloads should be placed in
    the input_data/ERA_data/ directory.

    Currently the software is set up to only run the first timestep 
    saved in any given ERA data file AND the ERA data files are 
    expected to be in netCDF (*.nc) format. Therefore, for each 
    timestep you would like to generate data for YOU NEED TO save the
    data for that timestep in it's own netCDF file.
    
    ---------- MODES Data ----------
    If you would like to aquire the data that was used in the paper 
    mentioned above the zenodo links are given below:

        https://doi.org/10.5281/zenodo.12726172
        https://doi.org/10.5281/zenodo.12724196
        https://doi.org/10.5281/zenodo.12749244
        https://doi.org/10.5281/zenodo.12749316
        https://doi.org/10.5281/zenodo.12749407
        https://doi.org/10.5281/zenodo.12749482
        https://doi.org/10.5281/zenodo.12751158
        https://doi.org/10.5281/zenodo.12751242
        https://doi.org/10.5281/zenodo.12751345
        https://doi.org/10.5281/zenodo.12751416

    To aquire your own MODES modal decomposition data you should 
    contact the Zagar group at the University of Hamburg who created 
    and maintains the MODES software package. The data you will need to
    aquire from them includes the vertical structure functions (VSF's),
    Hough functions and their associated frequencies, and the Hough 
    coefficients. These data should then be stored in the following 
    qMODES directories:

    vertical structure functions (VSFs)--> input_data/MODES_data/vsf/
    Hough functions and frequencies    --> input_data/MODES_data/hough/
    Hough coefficients                 --> input_data/MODES_data/coef/

    NOTE: The hough function files and frequency files should BOTH be
    stored in the input_data/MODES_data/hough/ directory.

------------------------ RUNNING THE SOFTWARE -------------------------

    Currently the qMODES software is configured so that a single run 
    produces values for a the first timestep of an single ERA5 data 
    file and it corresponding MODES decomposition data. A big picture 
    list of steps for how to perform a single run is as follows.

    -1. Make sure the ERA5 and MODES input data is downloaded as 
    described above.

    0.  Precompute the integrated vertical structure functions (VSF's) 
        using the /src/qMODES_scripts/Calculate_Integrated_VSFs.py 
        script and store them in the input_data/MODES_data/vsf_int/ 
        directory. Precomputing (and storing) these values allows this
        step to be skipped for future runs which use the same VSF's.

    1.  Compute the Fourier space (qk) values by running the script 
        /src/qMODES_scripts/Calculate_qk.py and store the results in
        /output_data/qk_data/. 
       
        When running the script in the command line you will need to 
        specify the '-d' and '-m' flags/parameters which are flags for 
        the date (in YYYYMMDD format) and MODE (EIG, WIG, or BAL) for 
        the given run. The script will attempt tosave data for each of 
        the different modes (EIG, WIG, or BAL) in the same file, as 
        long as a file for that date already exists.

    2.  Compute the physical space values (qMODES) by running the script
        /src/qMODES_scripts/Calculate_qMODES.py and store the results in
        /output_data/qMODES_data/

    At the moment the physical space and fourier space grid parameters 
    are hard coded into each of the scripts where they are relavent.
    Hopefully this will be fixed with an update soon.


----------------------- VERSION HISTORY COMMENTS ----------------------

    The current version is the initial commit. Comments on different 
    versions may appear here in later versions.


------------------------------- LISCENSE ------------------------------    

    The liscense for the qMODES software package is a standard Creative
    Commons 1.0 Liscense. For more information see the file titled 
    LISCENSE.md in the base directory.


----------------------------- CONTRIBUTORS ----------------------------

    Bradley Kumm, PhD 
    University of Wisconsin - Madison
    bkumm at wisc dot edu or brkumm at gmail dot com

    Valentino Neduhal
    University of Hamburg
    valentino dot neduhal at uni-hamburg dot de

    Sam Stechmann, PhD
    University of Wisconsin - Madison
    stechmann at wisc dot edu

    Nedjeljka Zagar, PhD
    University of Hamburg
    nedjeljka dot zagar at uni-hamburg dot de

--------------------------- ACKNOWLEDGEMENTS --------------------------

    Zagar Group and specifically, Nedjeljka Zagar and Valentino Neduhal
    For help obtaining the MODES software data which served as input to
    our qMODES package, and help with understanding this data, and also
    for their feedback and insights during this research project.

    ECMWF for producing and distributing the ERA5 reanalysis data sets.




