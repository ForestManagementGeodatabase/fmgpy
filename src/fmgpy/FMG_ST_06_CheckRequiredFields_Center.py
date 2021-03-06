# -*- coding: UTF-8 -*-

import arcpy
from FMG_QA_FunctionLibrary import check_required_fields_center
import os

# Get Parameter arguments for script tool
fc_center = arcpy.GetParameterAsText(0)
plot_name = arcpy.GetParameterAsText(1)
flag_name = arcpy.GetParameterAsText(2)


# Check each field collected dataset for required fields
check_required_fields_center(fc_center, plot_name, flag_name)
