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
    FC_Plots       --  Path to feature class of required plot locations
    Plots_PlotID   --  Field name of Plot ID column for required plot location feature class
    Age_FlagField  --  Field name of age requirement flag field for required plot location feature class
    FC_Age         --  Path to feature class of contractor submitted age plots
    Age_PlotID     --  Field name of Plot ID column for contractor submitted age plot feature class
    """

    # Check to ensure Age plots exit where required, adding and populating a flag field on the plot center feature class

    # Create dataframes
    center_df = pd.DataFrame.spatial.from_featureclass(fc_center)
    age_df = pd.DataFrame.spatial.from_featureclass(fc_age)

    # where age_flag_field = A in fc_center
    center_df["HAS_AGE"] = center_df[center_plot_id_field].isin(age_df[age_plot_id])
    arcpy.AddMessage("Plot points checked for corresponding age record")

    # TODO: save out dataframes
    # overwrite input FC
    return fc_center
