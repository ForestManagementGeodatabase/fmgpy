# -*- coding: UTF-8 -*-

import arcpy
from FMG_QA_FunctionLibrary import remove_duplicates
import os

# Get Parameter arguments for script tool
fc_prism = arcpy.GetParameterAsText(0)
fc_fixed = arcpy.GetParameterAsText(1)
fc_age = arcpy.GetParameterAsText(2)

# Verify required age trees have been collected
remove_duplicates(fc_prism, fc_fixed, fc_age)

                                                  
                                                  
