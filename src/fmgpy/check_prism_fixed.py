# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import pandas as pd
from bool_to_text import yes_no

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
    prism_df["HAS_FIXED"] = prism_df[prism_plot_id].isin(fixed_df[fixed_plot_id])
    yes_no(prism_df, 'HAS_FIXED')
    # check_df.loc[check_df['HAS_FIXED'] == 1, 'HAS_FIXED'] = "Yes"
    # check_df.loc[check_df['HAS_FIXED'] == 0, 'HAS_FIXED'] = "No"
    arcpy.AddMessage(
        "Prism points {0} checked for corresponding fixed points".format(fc_prism)
    )

    # flag fixed plot IDs without corresponding prism plot
    fixed_df["HAS_PRISM"] = fixed_df[fixed_plot_id].isin(prism_df[prism_plot_id])
    yes_no(fixed_df, 'HAS_PRISM')
    # check_df.loc[check_df['HAS_PRISM'] == 1, 'HAS_PRISM'] = "Yes"
    # check_df.loc[check_df['HAS_PRISM'] == 0, 'HAS_PRISM'] = "No"
    arcpy.AddMessage(
        "Fixed points {0} checked for corresponding prism points".format(fc_fixed)
    )

    # overwrite input FC
    prism_df.spatial.to_featureclass(fc_prism, sanitize_columns=False)
    fixed_df.spatial.to_featureclass(fc_fixed, sanitize_columns=False)
    return [fc_prism, fc_fixed]
