#-----------------------------------------------------------------------------
# IMPORTS
from .get_environment_variables import get_QMODES_REPO_DIR

import os
import yaml
from dataclasses import dataclass

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CLASS DEFINITION 

@dataclass
class qMODES_config_parameters:
    input_data_dir: str
    output_data_dir: str
    nplev: int
    nlat: int
    nlon: int
    nK: int
    nM: int
    nN: int
    ps0: float
    Omega: float

    # Convert relative paths to absolute paths using the QMODES_REPO_DIR environment variable
    def __post_init__(self):

        repo_dir = get_QMODES_REPO_DIR()

        # Adding base dir to input and output data directories if they are relative paths
        if isinstance(self.input_data_dir, str) and repo_dir not in self.input_data_dir:
            temp_path = os.path.join(repo_dir, self.input_data_dir)
            #clean up the path using os.path.normpath before updating input_data_dir
            self.input_data_dir = os.path.normpath(temp_path)

        if isinstance(self.output_data_dir, str) and repo_dir not in self.output_data_dir:
            temp_path = os.path.join(repo_dir, self.output_data_dir)
            #clean up the path using os.path.normpath before updating output_data_dir
            self.output_data_dir = os.path.normpath(temp_path)

    # Method to retrieve the default directory location for various model inputs and outputs
    def get_default_data_dir(self, data_type: str) -> str:
        """
        Returns the qMODES default directory location for various model inputs and outputs using the input_data_dir and output_data_dir values.
        Valid inputs for 'data_type' string are: 'ERA', 'coef', 'hough', 'freq', 'vsf', 'vsf_int', 'qk', 'qmodes', everything else will raise a ValueError.
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

        # raise error if the input data_type is not valid
        if data_type not in data_type_to_dict_map:
            raise ValueError(f"Input value for 'data_type' is not valid. Valid inputs are: {list(data_type_to_dict_map.keys())}")

        # Clean up the path using os.path.normpath
        return os.path.normpath(data_type_to_dict_map[data_type])
    
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