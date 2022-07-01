# -*- coding: UTF-8 -*-

import arcpy
from check_plot_id import check_plot_ids
import os

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
