import os, sys
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

# adding /src/fmgpy to the system path
module_folder_path = os.path.realpath('../src/fmgpy')
sys.path.insert(0, module_folder_path)

from FMG_QA_FunctionLibrary import check_plot_ids

test_folder = os.path.relpath("./tests/data/Pool_17_20210930/QA_Output.gdb")

test_folder_path = os.path.realpath(test_folder)

fc_age = os.path.join(test_folder_path, "Age")
age_df = pd.DataFrame.spatial.from_featureclass(fc_age)

fc_fixed = os.path.join(test_folder_path, "Fixed")
fixed_df = pd.DataFrame.spatial.from_featureclass(fc_fixed)

fc_prism = os.path.join(test_folder_path, "Prism")
prism_df = pd.DataFrame.spatial.from_featureclass(fc_prism)

fc_center = os.path.join(test_folder_path, "Plot_WGS84")
center_df = pd.DataFrame.spatial.from_featureclass(fc_center)

check_plot_ids(fc_center, 'PLOT', fc_fixed, 'plot')


def test_plot_id(df):
    assert "valid_plot_id" in list(df)
