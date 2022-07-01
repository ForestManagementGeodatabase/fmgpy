import arcpy
import os, sys, datetime

from bool_to_text import yes_no
from check_contractor_age_plots import check_contractor_age_plots
from check_fixed_offsets import check_fixed_offset
from check_plot_id import check_plot_ids
from check_prism_fixed import check_prism_fixed
from check_required_fields_age import check_required_fields_age
from check_required_fields_fixed import check_required_fields_fixed
from check_required_fields_prism import check_required_fields_prism


# define input datasets
inCenter = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Plot_WGS84"
inFixed = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Fixed"
inPrism = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Prism"
inAge = r"C:\GitHub_Repos\FMG\fmgpy\tests\data\Pool_17_20210930\QA_Output.gdb\Age"

# Check fixed plot IDs against Plot locations

# check_plot_ids(inCenter, 'PLOT', inFixed, 'PLOT')
# print('checked {0}'.format(os.path.basename(inFixed)))
#
# check_plot_ids(inCenter, 'PLOT', inPrism, 'PLOT')
# print('checked {0}'.format(os.path.basename(inPrism)))
#
# check_plot_ids(inCenter, 'PLOT', inAge, 'PLOT')
# print('checked {0}'.format(os.path.basename(inAge)))

# Check that prism plots have fixed plots and that fixed plots have prism plots
check_prism_fixed(inPrism, 'PLOT', inFixed, 'PLOT')
# Ran quickly and correctly


# Check that age plots have been collected as prescribed
# check_contractor_age_plots(FC_Plots=inPlot,
#                            Plots_PlotID='PLOT',
#                            Age_FlagField='Age',
#                            FC_Age=inAge,
#                            Age_PlotID='PLOT')
# Ran quickly and correctly, need to watch for the AGE field definition query
# without this being standardized the tool will be more error-prone


# Check that fixed plots are within 3 meters of plot center
# check_fixed_offset(FC_PlotLocations=inPlot,
#                    PlotID_Field='PLOT',
#                    FC_Fixed=inFixed,
#                    Fixed_PlotID_Field='plot')
# Ran quickly and correctly - need to pay attention to magnitude of offset:
# large offsets can indicate that the fixed plot has the wrong plot ID


# Check Missing fields for Prism Points
# check_required_fields_prism(inPrism)
# Ran quickly and correctly


# Check missing fields for Age points
# check_required_fields_age(inAge)
# Ran quickly and correctly


# Check missing fields for Fixed points
# check_required_fields_fixed(inFixed)
# Ran Quickly and correctly
