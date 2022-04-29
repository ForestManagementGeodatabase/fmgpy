# from fmgpy.check_plot_id import check_plot_id
import os
import arcpy

test_folder = relative_path = os.path.relpath("./data/Pool_17_20210930")

test_folder_real = os.path.realpath(test_folder)

age_path = os.path.join(test_folder_real, "Age.shp")

age = arcpy.MakeFeatureLayer_management(age_path, "age")

