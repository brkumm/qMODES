from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
import numpy as np


class nlcmap(LinearSegmentedColormap):
    """A nonlinear colormap"""

    name = 'nlcmap'

    def __init__(self, cmap, levels):
        self.cmap = cmap
        self.monochrome = self.cmap.monochrome
        self.levels = np.asarray(levels, dtype='float64')
        self._x = self.levels - self.levels.min()
        self._x /= self._x.max()
        self._y = np.linspace(0, 1, len(self.levels))

    def __call__(self, xi, alpha=1.0, **kw):
        yi = np.interp(xi, self._x, self._y)
        return self.cmap(yi, alpha)




cm_my = [[0.16048622, 0.22842497, 0.55420386],
         [0.09884412, 0.32190111, 0.73617986],
         [0.08481877, 0.43940606, 0.73613168],
         [0.52418488, 0.69527879, 0.75528737],
         [0.68147106, 0.77010319, 0.80092296],
         [1, 1, 1],
         [0.90689709, 0.68154344, 0.62377885],
         [0.8693981, 0.55654448, 0.4667218],
         [0.78924224, 0.31139994, 0.20148645],
         [0.72467839, 0.16813609, 0.14138745],
         [0.608005, 0.06275633, 0.16024132]]


def get_continuous_cmap(rgb_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list.

        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.

        Returns
        ----------
        colour map'''
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp

def get_my_colormap(lvls):
    cmap_nonlin = nlcmap(get_continuous_cmap(cm_my), lvls)
    return cmap_nonlin





