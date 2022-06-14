import arcpy
import os, sys, datetime
import FMG_QA_FunctionLibrary

# Define some input datasets
inCenter = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Plot_WGS84"
inFixed = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Fixed"
inPrism = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Prism"
inAge = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Age"

# Check fixed plot IDs against Plot locations

# FMG_QA_FunctionLibrary.check_Plot_IDs(inCenter, 'PLOT', inFixed, 'PLOT')
# print('checked {0}'.format(os.path.basename(inFixed)))
#
# FMG_QA_FunctionLibrary.check_Plot_IDs(inCenter, 'PLOT', inPrism, 'PLOT')
# print('checked {0}'.format(os.path.basename(inPrism)))
#
# FMG_QA_FunctionLibrary.check_Plot_IDs(inCenter, 'PLOT', inAge, 'PLOT')
# print('checked {0}'.format(os.path.basename(inAge)))

# Check that prism plots have fixed plots and that fixed plots have prism plots
FMG_QA_FunctionLibrary.check_Prism_Fixed(inPrism, 'PLOT', inFixed, 'PLOT')
# Ran quickly and correctly


# Check that age plots have been collected as prescribed
# FMG_QA_FunctionLibrary.check_Contractor_Age_Plots(FC_Plots=inPlot,
#                                                  Plots_PlotID='PLOT',
#                                                  Age_FlagField='Age',
#                                                  FC_Age=inAge,
#                                                  Age_PlotID='PLOT')
# Ran quickly and correctly, need to watch for the AGE field definition query
# without this being standardized the tool will be more error-prone


# Check that fixed plots are within 3 meters of plot center
# FMG_QA_FunctionLibrary.check_Fixed_Offset(FC_PlotLocations=inPlot,
#                                           PlotID_Field='PLOT',
#                                           FC_Fixed=inFixed,
#                                           Fixed_PlotID_Field='plot')
# Ran quickly and correctly - need to pay attention to magnitude of offset:
# large offsets can indicate that the fixed plot has the wrong plot ID


# Check Missing fields for Prism Points
# FMG_QA_FunctionLibrary.check_Required_Fields_Prism(inPrism)
# Ran quickly and correctly


# Check missing fields for Age points
# FMG_QA_FunctionLibrary.check_Required_Fields_Age(inAge)
# Ran quickly and correctly


# Check missing fields for Fixed points
# FMG_QA_FunctionLibrary.check_Required_Fields_Fixed(inFixed)
# Ran Quickly and correctly
