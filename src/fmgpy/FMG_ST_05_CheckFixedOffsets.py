# -*- coding: UTF-8 -*-

import arcpy
from check_fixed_offsets import check_fixed_offset
import os

# Get Parameter arguments for script tool
fc_center = arcpy.GetParameterAsText(0)
center_plot_id_field = arcpy.GetParameterAsText(1)
fc_fixed = arcpy.GetParameterAsText(2)
fixed_plot_id_field = arcpy.GetParameterAsText(3)

# Check fixed plot offset from plot centers
check_fixed_offset(fc_center, center_plot_id_field, fc_fixed, fixed_plot_id_field)
