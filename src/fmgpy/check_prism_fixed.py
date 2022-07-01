# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

arcpy.env.overwriteOutput = True


def check_prism_fixed(fc_prism, prism_plot_id, fc_fixed, fixed_plot_id):
    """ Checks to make sure there is a prism plot for every fixed plot and that there is a
    fixed plot for each prism plot. This is accomplished by comparing unique sets of plot
    IDs present for each feature class and populating fields indicating if this relationship
    holds true

    Keyword Arguments:
    fc_prism        -- Path to prism feature class
    prism_plot_id   -- Prism feature class plot ID field
    fc_fixed        -- Path to fixed plot feature class
    fixed_plot_id   -- Fixed feature class plot ID field
    """

    arcpy.AddMessage(
        "Checking for existence of corresponding prism and fixed plots"
    )

    # create dataframes
    prism_df = pd.DataFrame.spatial.from_featureclass(fc_prism)
    fixed_df = pd.DataFrame.spatial.from_featureclass(fc_fixed)

    # flag prism plot IDs without corresponding fixed plot
    prism_df["has_fixed"] = prism_df[prism_plot_id].isin(fixed_df[fixed_plot_id])
    arcpy.AddMessage(
        "Prism points {0} checked for corresponding fixed points".format(fc_prism)
    )

    # flag fixed plot IDs without corresponding prism plot
    fixed_df["has_prism"] = fixed_df[fixed_plot_id].isin(prism_df[prism_plot_id])
    arcpy.AddMessage(
        "Fixed points {0} checked for corresponding prism points".format(fc_fixed)
    )

    # overwrite input FC
    prism_df.spatial.to_featureclass(fc_prism, sanitize_columns=False)
    fixed_df.spatial.to_featureclass(fc_fixed, sanitize_columns=False)
    return [fc_prism, fc_fixed]
