# from fmgpy.check_plot_id import check_plot_id
import os
import arcpy

test_folder = os.path.relpath("./data/Pool_17_20210930")

test_folder_path = os.path.realpath(test_folder)

age_path = os.path.join(test_folder_path, "Age.shp")
age = arcpy.MakeFeatureLayer_management(age_path, "age")

fixed_path = os.path.join(test_folder_path, "Fixed.shp")
fixed = arcpy.MakeFeatureLayer_management(fixed_path, "fixed")

prism_path = os.path.join(test_folder_path, "Prism.shp")
prism = arcpy.MakeFeatureLayer_management(prism_path, "prism")
