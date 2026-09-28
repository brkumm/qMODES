#-----------------------------------------------------------------------------
# IMPORTS
import os
import xarray as xa
import glob

from .qMODES_config_parameters import load_qmodes_config
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# FUNCTIONS
def get_klb_kub_ktot_from_qk_filename(filename: str) -> tuple[int, int, int]:
    # input should only be the filename ... no path info.
    rep_filename = filename.replace("-", "_")
    filename_split_list = rep_filename.split("_")

    klb  = filename_split_list[3]
    kub  = filename_split_list[5]
    ktot = filename_split_list[7].split(".")[0]

    return int(klb), int(kub), int(ktot)


def get_qk_files_with_date_and_ktot(date: str, ktot: str,
                                    config_file: str) -> list[str]:

    config_params = load_qmodes_config(config_file)
    pattern = config_params.get_default_file_pattern('qk', date, ktot)

    return glob.glob(pattern)



def check_qk_files_cover_ktot_range(file_list: list[str], 
                                    config_file: str) -> bool:

    config_params = load_qmodes_config(config_file)
    ktot = config_params.nK
    ktot_range = set([i for i in range(ktot)])

    for fname in file_list:
        klb, kub, _ = get_klb_kub_ktot_from_qk_filename( os.path.basename(fname) )

        for ik in range(klb, kub+1):
            if ik in ktot_range: ktot_range.remove(ik)
            else:
                print(f"ERROR: To combine qk files no files should overlap in k values or be greater than {ktot}.")
                print(f"The k value {ik} violates one of both of these.")
                
    # if all values removed from ktot one time range is covered
    if not ktot_range: 
        return True

    else:
        print("ERROR: Not all k values are covered by the following files")
        for fname in file_list: print(f"\t{fname}")
        return False



def check_qk_files_have_all_modes(file_list: list[str]) -> bool:

    var_set = {"qk_EIG","qk_WIG","qk_BAL"}
    is_first_error = True

    for fname in file_list:

        fname_ds = xa.open_dataset(fname)
        var_set = {"qk_EIG","qk_WIG","qk_BAL"}
        for var in list( fname_ds.data_vars.keys() ):

            if var in var_set: 
                var_set.remove(var)

            else:

                if is_first_error:
                    print("ERROR: The following errors were found while examining qk files\n")
                    is_first_error = False

                print(f"\t{fname}: {var}  data variable found when data vars should only include qk_EIG, qk_WIG, or qk_BAL\n")

        if var_set:

            if is_first_error:
                    print("ERROR: The following errors were found while examining qk files\n")
                    is_first_error = False

            print(f"\t{fname}: Doesn't have all necessary modes\n")

    if is_first_error: return True
    else: return False



def combine_qk_files_from_list(file_list: list[str], output_filename: str) -> None:
    combined_ds = xa.open_mfdataset(file_list, combine="by_coords")
    combined_ds.to_netcdf(output_filename)

    print(f"\nFiles combined and saved to:\n\t{output_filename}\n")

    return
#-----------------------------------------------------------------------------
