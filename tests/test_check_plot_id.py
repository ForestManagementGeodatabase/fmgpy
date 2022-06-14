import os, sys
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

# adding /src/fmgpy to the system path
module_folder_path = os.path.realpath('../src/fmgpy')
sys.path.insert(0, module_folder_path)

from check_plot_id import check_plot_ids

test_folder = os.path.relpath("./tests/data/Pool_17_20210930/QA_Output.gdb")

test_folder_path = os.path.realpath(test_folder)

age_path = os.path.join(test_folder_path, "Age")
age_df = pd.DataFrame.spatial.from_featureclass(age_path)

fixed_path = os.path.join(test_folder_path, "Fixed")
fixed_df = pd.DataFrame.spatial.from_featureclass(fixed_path)

prism_path = os.path.join(test_folder_path, "Prism")
prism_df = pd.DataFrame.spatial.from_featureclass(prism_path)

center_path = os.path.join(test_folder_path, "Plot_WGS84")
center_df = pd.DataFrame.spatial.from_featureclass(center_path)

check_plot_ids(center_path, 'PLOT', fixed_path, 'plot')


def test_plot_id(df):
    assert "valid_plot_id" in list(df)
