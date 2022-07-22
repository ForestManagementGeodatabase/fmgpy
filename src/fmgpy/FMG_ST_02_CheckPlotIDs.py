# -*- coding: UTF-8 -*-

import arcpy
from FMG_QA_FunctionLibrary import check_plot_ids

# Get Parameter arguments for script tool
fc_center = arcpy.GetParameterAsText(0)
center_plot_id_field = arcpy.GetParameterAsText(1)
fc_check = arcpy.GetParameterAsText(2)
check_plot_id_field = arcpy.GetParameterAsText(3)

# Check PlotIDs
check_plot_ids(fc_center,
               center_plot_id_field,
               fc_check,
               check_plot_id_field)
