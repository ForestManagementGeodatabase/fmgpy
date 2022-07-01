# -*- coding: UTF-8 -*-

import arcpy
from check_required_fields_prism import check_required_fields_prism
from check_required_fields_age import check_required_fields_age
from check_required_fields_fixed import check_required_fields_fixed
import os

# Get Parameter arguments for script tool
fc_prism = arcpy.GetParameterAsText(0)
fc_age = arcpy.GetParameterAsText(1)
fc_fixed = arcpy.GetParameterAsText(2)

# Check each field collected dataset for required fields
check_required_fields_prism(fc_prism)

check_required_fields_age(fc_age)

check_required_fields_fixed(fc_fixed)
