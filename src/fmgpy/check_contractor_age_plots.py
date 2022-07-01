# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

arcpy.env.overwriteOutput = True


def check_contractor_age_plots(fc_center, center_plot_id_field, age_flag_field, fc_age, age_plot_id):
    """Checks prescribed age plots against collected age plots. Returns the prescribed age
    plots with a flag field indicating if an age plot was collected.

    Keyword Arguments:
    fc_center               --  Path to feature class of required plot locations
    center_plot_id_field    --  Field name of Plot ID column for required plot location feature class
    age_flag_field          --  Field name of age requirement flag field for required plot location feature class
    fc_age                  --  Path to feature class of contractor submitted age plots
    age_plot_id             --  Field name of Plot ID column for contractor submitted age plot feature class
    """

    # check to ensure Age plots exit where required, adding and populating a flag field on the plot center feature class

    # create dataframes
    center_df = pd.DataFrame.spatial.from_featureclass(fc_center)
    age_df = pd.DataFrame.spatial.from_featureclass(fc_age)

    # populate HAS_AGE field for each plot where age_flag_field = A
    center_df.loc[center_df[age_flag_field] == 'A', 'HAS_AGE'] = center_df[center_plot_id_field].isin(age_df[age_plot_id])
    arcpy.AddMessage("Plot points checked for corresponding age record")

    # overwrite input FC
    center_df.spatial.to_featureclass(fc_center, sanitize_columns=False)
    return fc_center
