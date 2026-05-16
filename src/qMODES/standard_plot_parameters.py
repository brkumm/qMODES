import numpy as np

qmodes_contour_levels = {'qERA': np.linspace(-10.0, 10.0,21),
						 'qROT': np.linspace(-4.0,  4.0, 21),
						 'qIG' : np.linspace(-2.0,  2.0, 21),
						 'qM'  : np.linspace(-10.0, 10.0,21) }

qmodes_updated_contour_levels = {'qERA': np.linspace(-5.0,  5.0, 21),
                                 'qROT': np.linspace(-2.0,  2.0, 21),
                                 'qIG' : np.linspace(-1.0,  1.0, 21),
                                 'qM'  : np.linspace(-5.0,  5.0, 21) }

qmodes_mode_plot_colors = {'qERA':'blue', 'qROT':'green', 
                           'qIG':'orange', 'qM':'red' }	