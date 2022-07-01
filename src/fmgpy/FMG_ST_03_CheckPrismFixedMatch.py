# -*- coding: UTF-8 -*-

import arcpy
from check_prism_fixed import check_prism_fixed
import os

# Get Parameter arguments for script tool
fc_prism = arcpy.GetParameterAsText(0)
prism_plot_id = arcpy.GetParameterAsText(1)
fc_fixed = arcpy.GetParameterAsText(2)
fixed_plot_id = arcpy.GetParameterAsText(3)

# Check each fixed plot has a prism plot and each prism plot has a fixed plot
check_prism_fixed(fc_prism, prism_plot_id, fc_fixed, fixed_plot_id)


                                         
