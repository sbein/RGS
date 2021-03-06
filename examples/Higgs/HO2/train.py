#!/usr/bin/env python
# -----------------------------------------------------------------------------
#  File:        train.py
#  Description: HO2 optimization example
#  Created:     10-Jan-2015 Harrison B. Prosper and Sezen Sekmen
#  Updated:     17-Jun-2017 HBP get ready for release
# -----------------------------------------------------------------------------
import os, sys, re
from rgsutil import *
from string import *
from ROOT import *
# -----------------------------------------------------------------------------
# read scale factors
execfile('../../data/scales.py')

def main():
    NAME = "HO2"
    print "="*80
    print "\t=== %s ===" % NAME
    print "="*80

    # ---------------------------------------------------------------------
    # Load the RGS shared library and check that the various input files
    # exist.
    # ---------------------------------------------------------------------
    gSystem.AddDynamicPath('$RGS_PATH/lib')
    if gSystem.Load("libRGS") < 0: error("unable to load libRGS")

    # Name of file containing cut definitions
    # Format of file:
    #   variable-name  cut-type (>, <, <>, |>, |<, ==)
    varfilename = "%s.cuts" % NAME
    if not os.path.exists(varfilename):
        error("unable to open variables file %s" % varfilename)

    # Files to be processed
    filename1 = "../../data/ntuple_HZZ4L_VBF.root"
    if not os.path.exists(filename1):
        error("unable to open file %s" % filename1)

    filename2 = "../../data/ntuple_HZZ4L.root"
    if not os.path.exists(filename2):
        error("unable to open file %s" % filename2)

    filename3 = "../../data/ntuple_ZZ4L.root"
    if not os.path.exists(filename3):
        error("unable to open file %s" % filename3)        

    # ---------------------------------------------------------------------
    #  Create RGS object
    #  
    #   The file (cutdatafilename) of cut-points is usually a signal file,
    #   which ideally differs from the signal file on which the RGS
    #   algorithm is run.
    # ---------------------------------------------------------------------
    cutdatafilename = filename1
    start      = 0           # start row 
    maxcuts    = 10000       # maximum number of cut-points to consider
    treename   = "Analysis"  # name of Root tree 
    weightname = "weight"    # name of event weight variable
    selection  = \
      "(mass4l <= 150) &&" \
      "(mass4l >= 100)"
    rgs = RGS(cutdatafilename, start, maxcuts, treename,
                  weightname, selection)

    # ---------------------------------------------------------------------
    #  Add signal and background data to RGS object.
    #  Weight each event using the value in the field weightname, if
    #  present.
    #  NB: We asssume all files are of the same format.
    # ---------------------------------------------------------------------
    # 1) The first optional argument is a string, which, if given, will be
    # appended to the "count" and "fraction" variables. The "count" variable
    # contains the number of events that pass per cut-point, while "fraction"
    # is count / total, where total is the total number of events per file.
    # If no string is given, the default is to append an integer to the
    # "count" and "fraction" variables, starting at 0, in the order in which
    # the files are added to the RGS object.
    # 2) The second optional argument is the weight to be assigned per file. If
    # omitted the default weight is 1.
    # 3) The third optional argument is the selection string. If omitted, the
    # selection provided in the constructor is used.
    
    start    = 0   #  start row
    numrows  =-1   #  scan all the data from the files

    rgs.add(filename1, start, numrows, "_VBF", VBFscale)
    rgs.add(filename2, start, numrows, "_ggF", ggFscale)
    rgs.add(filename3, start, numrows, "_ZZ",  ZZscale)

    # ---------------------------------------------------------------------	
    #  Run RGS and write out results
    # ---------------------------------------------------------------------	    
    rgs.run(varfilename)

    # Write to a root file
    rgsfilename = "%s.root" % NAME
    rgs.save(rgsfilename)
# -----------------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "\tciao!\n"



