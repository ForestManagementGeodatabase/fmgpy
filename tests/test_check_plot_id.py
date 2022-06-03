# from fmgpy.check_plot_id import check_plot_id
import os
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

test_folder = os.path.relpath("./tests/data/Pool_17_20210930/QA_Output.gdb")

test_folder_path = os.path.realpath(test_folder)

age_path = os.path.join(test_folder_path, "Age")
age_df = pd.DataFrame.spatial.from_featureclass(age_path)

fixed_path = os.path.join(test_folder_path, "Fixed")
fixed_df = pd.DataFrame.spatial.from_featureclass(fixed_path)

prism_path = os.path.join(test_folder_path, "Prism")
prism_df = pd.DataFrame.spatial.from_featureclass(prism_path)

plot_path = os.path.join(test_folder_path, "Plot")
plot_df = pd.DataFrame.spatial.from_featureclass(plot_path)

# saving out to feature class, output must be same type as original input
# i.e. if input is a shapefile, output can't be a gdb feature class

age_path_2 = os.path.join(test_folder_path, "Age_2")
age_df.spatial.to_featureclass(age_path_2)

Check_PlotID_Field = "PLOT"
