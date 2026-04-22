#-------------------------------------------------------------------------
# Script: math_util.py
# Author: Bradley Kumm (brkumm@gmail.com)
# Creation Date: 2026/01/14
# Description: This script contains custom math functions for analyzing 
#              data using the qMODES Framework
# Notes: 
#
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Imports

import numpy  as np

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# MY DERIVATIVE FUNCTIONS TO ENSURE I KNOW EXACTLY WHAT THEY ARE DOING

def qMODES_deriv(xvals, yvals):
    """
    Custom derivative function that appriximates derivative at the first
    and last data points in the usual way but uses qMODES_deriv_at_point 
    for all other xvalues. This is important for non equal grid spacings.
    """
    ny = len(yvals)
    deriv = np.zeros(ny)

    # deriv at first point
    deriv[0] = (yvals[1] - yvals[0]) / (xvals[1]-xvals[0])

    for i in range(1,ny-1):
        plist = [ (xvals[i-1],yvals[i-1]), (xvals[i],yvals[i]), (xvals[i+1],yvals[i+1]) ]
        deriv[i] = qMODES_deriv_at_point(plist,xvals[i])

    # deriv at last point
    deriv[ny-1] = (yvals[ny-1] - yvals[ny-2]) / (xvals[ny-1] - xvals[ny-2])

    return deriv

def qMODES_deriv_at_point(points_list,xval):
    """
    This function calculates the derivative at the given point xval, from
    the three points given in points list. Calculated by finding the 
    coefficients a,b, and c that solve for the 2nd order polynomial that 
    passes through the points in the points_list (f(x) = ax^2 + bx + c)
    then the derivative of this polynomial (2ax + b) should give an good 
    approximation of the derivative in the range 
    [min(x1,x2,x3), max(x1,x2,x3)]

    NOTE: no warnings or errors if xval is outside the range
          [min(x1,x2,x3), max(x1,x2,x3)]
    """
    x1 = float( points_list[0][0] ) 
    x2 = float( points_list[1][0] ) 
    x3 = float( points_list[2][0] )

    y1 = float( points_list[0][1] ) 
    y2 = float( points_list[1][1] ) 
    y3 = float( points_list[2][1] ) 

    if len(set(x1,x2,x3)) != 3:
        raise ZeroDivisionError("Repeated x-values causes ZeroDivisionError")

    a = ( x1 * ( y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1) ) / ((x1 - x2)*(x1 - x3)*(x2 - x3))
    b = (y2 - y1) / (x2 - x1)  - a * (x1 + x2)
    #c coefficient doesn't matter after taking deriv 

    return 2.0 * a * float(xval) + b

#-------------------------------------------------------------------------
