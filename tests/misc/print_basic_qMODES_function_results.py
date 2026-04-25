from qMODES import get_QMODES_ERA_DIR, get_QMODES_MODES_DIR, get_QMODES_COEF_DIR, get_QMODES_VSF_DIR, get_QMODES_VSFINT_DIR, get_QMODES_COEF_DIR, get_QMODES_QKDATA_DIR, get_QMODES_QMODESDATA_DIR, get_QMODES_PLOTS_DIR

print(f"\nTESTING: read_environment_variables.py imports")
print(f"\tget_QMODES_ERA_DIR() returns:        {get_QMODES_ERA_DIR()}")
print(f"\tget_QMODES_MODES_DIR() returns:      {get_QMODES_MODES_DIR()}")
print(f"\tget_QMODES_COEF_DIR() returns:       {get_QMODES_COEF_DIR()}")
print(f"\tget_QMODES_VSF_DIR() returns:        {get_QMODES_VSF_DIR()}")
print(f"\tget_QMODES_VSFINT_DIR() returns:     {get_QMODES_VSFINT_DIR()}")
print(f"\tget_QMODES_COEF_DIR() returns:       {get_QMODES_COEF_DIR()}")
print(f"\tget_QMODES_QKDATA_DIR() returns:     {get_QMODES_QKDATA_DIR()}")
print(f"\tget_QMODES_QMODESDATA_DIR() returns: {get_QMODES_QMODESDATA_DIR()}")
print(f"\tget_QMODES_PLOTS_DIR() returns:      {get_QMODES_PLOTS_DIR()}")
print("\n")

from qMODES import sample_vsf_file, sample_vsf_int_file, sample_coef_file, sample_hough_file, sample_freq_file, sample_ERA_file

print(f"\nTESTING: sample_files.py imports")
print(f"\tsample_vsf_file()     returns: {sample_vsf_file()}")
print(f"\tsample_vsf_int_file() returns: {sample_vsf_int_file()}")
print(f"\tsample_coef_file()    returns: {sample_coef_file()}")
print(f"\tsample_hough_file()   returns: {sample_hough_file()}")
print(f"\tsample_freq_file()    returns: {sample_freq_file()}")
print(f"\tsample_ERA_file()     returns: {sample_ERA_file()}")
print("\n")

from qMODES import nK, nM, nN, nplev, nlat, nlon, ps0, Omega

print(f"\nTESTING: parameter.py imports")
print(f"nK returns:    {nK}")
print(f"nM returns:    {nM}")
print(f"nN returns:    {nN}")
print(f"nplev returns: {nplev}")
print(f"nlat returns:  {nlat}")
print(f"nlon returns:  {nlon}")
print(f"ps0 returns:   {ps0}")
print(f"Omega returns: {Omega}")
print("\n")

from qMODES import template_vsf_fname, template_vsf_int_fname, template_hough_fname, template_coef_fname, template_freq_fname, template_qk_fname, template_qmodes_fname, template_qk_with_klb_kub_ktot_fname, template_qmodes_with_klb_kub_ktot_fname, template_ERA_fname

print(f"\nTESTING: templates.py imports with dummy var inputs:")
print(f"template_vsf_fname()                 returns: {template_vsf_fname()}")
print(f"template_vsf_int_fname()             returns: {template_vsf_int_fname()}")
print(f"template_hough_fname()               returns: {template_hough_fname('001')}")
print(f"template_coef_fname()                returns: {template_coef_fname('20180801')}")
print(f"template_freq_fname()                returns: {template_freq_fname('001')}")
print(f"template_qk_fname()                  returns: {template_qk_fname('20180801')}")
print(f"template_qk_with_klb_kub_fname()     returns: {template_qk_with_klb_kub_ktot_fname('20180801', '001', '002', '351')}")
print(f"template_qmodes_with_klb_kub_fname() returns: {template_qmodes_with_klb_kub_ktot_fname('20180801', '001', '002', '351')}")
print(f"template_qmodes_fname()              returns: {template_qmodes_fname('20180801')}")
print(f"template_ERA_fname()                 returns: {template_ERA_fname('20180801')}")
print("\n")

from qMODES import qMODES_deriv, qMODES_deriv_at_point

xvals = [1,2,3,4,5]
yvals = [1,4,9,16,25]

points_list = [(1,1),(2,4),(3,9)]
xval        = 2

print(f"\nTESTING: math_util.py imports with dummy var inputs:")
print(f"qMODES_deriv(xvals,yvals)               returns: {qMODES_deriv(xvals,yvals)}")
print(f"qMODES_deriv_at_point(points_list,xval) returns: {qMODES_deriv_at_point(points_list,xval)}")
print("\n")

