#-----------------------------------------------------------------------------
# IMPORTS
import os

from dataclasses import dataclass
import yaml

from .get_environment_variables import get_QMODES_REPO_DIR

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CLASS DEFINITION, INITIALIZATION, METHODS, ETC...

@dataclass
class qMODES_config_parameters:
    input_data_dir: str
    output_data_dir: str
    t_start:str
    delta_t: int
    nT: int
    nplev: int
    nlat: int
    nlon: int
    nK: int
    nM: int
    nN: int
    ps0: float
    omega: float


    def __post_init__(self):

        # Convert relative paths to absolute paths using the QMODES_REPO_DIR environment variable
        repo_dir = get_QMODES_REPO_DIR()

        if isinstance(self.input_data_dir, str) and repo_dir not in self.input_data_dir:
            temp_path = os.path.join(repo_dir, self.input_data_dir)
            self.input_data_dir = os.path.normpath(temp_path)

        if isinstance(self.output_data_dir, str) and repo_dir not in self.output_data_dir:
            temp_path = os.path.join(repo_dir, self.output_data_dir)
            self.output_data_dir = os.path.normpath(temp_path)


    def get_default_data_dir(self, data_type: str) -> str:
        """
        Returns the qMODES default directory location for various model inputs and outputs using the input_data_dir and output_data_dir values.
        
        Valid inputs for 'data_type' string are: 
            ERA
            coef
            hough
            freq
            vsf 
            vsf_int
            qk
            qmodes
        
        All other inputs will raise a ValueError.
        NOTE: By default the frequency (freq) data is stored hough directory, and vsf_int data is stored vsf directory.
        """

        data_type_to_dict_map = {
            "ERA": f"{self.input_data_dir}/ERA_data/",
            "coef": f"{self.input_data_dir}/MODES_data/coef/",
            "hough": f"{self.input_data_dir}/MODES_data/hough/",
            "freq": f"{self.input_data_dir}/MODES_data/hough/",
            "vsf": f"{self.input_data_dir}/MODES_data/vsf/",
            "vsf_int": f"{self.input_data_dir}/MODES_data/vsf/",
            "qk": f"{self.output_data_dir}/qk_data/",
            "qmodes": f"{self.output_data_dir}/qmodes_data/"
        }

        # input checks
        if data_type not in data_type_to_dict_map:
            raise ValueError(f"Input value for 'data_type' is not valid. Valid inputs are: {list(data_type_to_dict_map.keys())}")

        # Clean up the path using os.path.normpath
        return os.path.normpath(data_type_to_dict_map[data_type])
    

    def get_default_file_path(self, file_type: str, date: str = None, 
                              k_str: str = None, klb_str: str = None, 
                              kub_str: str = None, ktot_str: str = None) -> str:
        """
        Returns the path (default convention) to a file for a given file 
        type, and additional arguments (depending on the file type).
        NOTE(S): 
        
        Valid inputs (as a string) for the  file types variable are: 
            ERA_q_fname, ERA_uv_fname, vsf_fname, 
            vsf_int_fname
            hough_fname
            coef_fname
            freq_fname
            qk_fname
            qmodes_fname

        Additional inputs (depending on the file type) are:
            date: date in YYYYMMDD format as a string.
            k_str: Single k-value in string format.
            klb_str: Lower bound of k value in file in string format.
            kub_str: Upper bound of k value in file in string format.
            ktot_str: Total number of k values in the run, formatted as a string (leading zeros if necessary)
        """

        file_type_to_path_dict = {
                    "ERA_q_fname": f"{self.input_data_dir}/ERA_data/ERA5_{date}_q-t_pl_data.nc",
                    "ERA_uv_fname": f"{self.input_data_dir}/ERA_data/ERA5_{date}_u-v_pl_data.nc",
                    "coef_fname": f"{self.input_data_dir}/MODES_data/coef/Hough_coeff_M60_F320_{date}0000000.nc",
                    "vsf_fname": f"{self.input_data_dir}/MODES_data/vsf/vsf.data.nc",
                    "vsf_int_fname": f"{self.input_data_dir}/MODES_data/vsf/vsf_int.data.nc",
                    "hough_fname": f"{self.input_data_dir}/MODES_data/hough/hough_F320_M60.wn00{k_str}.nc",
                    "freq_fname": f"{self.input_data_dir}/MODES_data/hough/freq_F320_{k_str}0000000.nc",
                    "qk_fname": f"{self.output_data_dir}/qk_data/qk_{date}0000000_klb-{klb_str}_kub-{kub_str}_ktot-{ktot_str}.nc",
                    "qmodes_fname": f"{self.output_data_dir}/qmodes_data/qmodes_{date}0000000_klb-{klb_str}_kub-{kub_str}_ktot-{ktot_str}.nc"
                }
        
        # Input checks
        if file_type not in file_type_to_path_dict:
            raise ValueError(f"Invalid input for file_type variable. Valid inputs are: {'\n\t'.join(file_type_to_path_dict.keys())}")

        elif file_type in ["ERA_q_fname", "ERA_uv_fname", "coef_fname"] and not isinstance(date, str):
            raise ValueError(f"{file_type} file_type requires the following input variables:\'date\'.")
        
        elif file_type in ["hough_fname", "freq_fname"] and not isinstance(k_str, str):
            raise ValueError(f"{file_type} file_type requires the following input variables:\'k_str\'.")
        
        elif file_type in ["qk_fname", "qmodes_fname"] and ( None in [date, klb_str, kub_str, ktot_str] ):
            raise ValueError(f"{file_type} file_type requires the following input variables: \'date\', \'klb_str\', \'kub_str\', \'ktot_str\'.")

        # return cleaned up string
        return os.path.normpath(file_type_to_path_dict[file_type])


    def get_default_file_pattern(self, pattern_type: str, date: str, ktot_str: str) -> str:
        """
        Returns the default file pattern for a given pattern type, date, and ktot value 
        NOTE: 

        Valid inputs (as a string) for the  file types variable are: 
            qk_file_pattern
            qmodes_file_pattern

        Additional required inputs:
            date (in YYYYMMDD format as a string)
            ktot total number of k values, as a string of length 3 (leading zeros if necessary)
        """

        pattern_type_to_pattern_dict = {
            "qk_file_pattern": f"{self.output_data_dir}/qk_data/qk_{date}0000000_klb-*_kub-*_ktot-{ktot_str}.nc",
            "qmodes_file_pattern": f"{self.output_data_dir}/qmodes_data/qmodes_{date}0000000_klb-*_kub-*_ktot-{ktot_str}.nc"
        }

        # Input check
        if pattern_type not in pattern_type_to_pattern_dict:
            raise ValueError(f"Invalid input for pattern_type variable. Valid inputs are: {' '.join(pattern_type_to_pattern_dict.keys())}")

        return os.path.normpath(pattern_type_to_pattern_dict[pattern_type])
    
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# FUNCTION TO LOAD qMODES_config_parameters FROM A GIVEN YAML FILE

def load_qmodes_config(file_path: str) -> qMODES_config_parameters:
    """Reads a YAML configuration file and returns a qMODES_config_parameters 
    instance."""

    with open(file_path, "r") as f:
        config_dict = yaml.safe_load(f)
        
    # The ** operator unpacks the dictionary.
    return qMODES_config_parameters(**config_dict)

#-----------------------------------------------------------------------------