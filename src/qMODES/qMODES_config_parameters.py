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
            self.input_data_dir = os.path.join(repo_dir, self.input_data_dir)
        if isinstance(self.output_data_dir, str) and repo_dir not in self.output_data_dir:
            self.output_data_dir = os.path.join(repo_dir, self.output_data_dir)

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# FUNCTION TO LOAD qMODES_config_parameters FROM A YAML FILE

def load_qmodes_config(file_path: str) -> qMODES_config_parameters:
    """Reads a YAML configuration file and returns a qMODES_config_parameters 
    instance."""

    with open(file_path, "r") as f:
        config_dict = yaml.safe_load(f)
        
    # The ** operator unpacks the dictionary.
    print(config_dict)
    return qMODES_config_parameters(**config_dict)

#-----------------------------------------------------------------------------