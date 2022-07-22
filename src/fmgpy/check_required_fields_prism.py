# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import sys
import pandas as pd
import numpy as np

from arcgis.features import GeoAccessor, GeoSeriesAccessor

arcpy.env.overwriteOutput = True


def check_required_fields_prism(fc_prism):
    """Checks prism plots for presence of required fields and for missing values in those fields.

    Keyword Arguments:
    fc_prism    -- Path to prism feature class
    """

    arcpy.AddMessage("Begin check on Prism points")

    # list of required fields
    rf_prism = [
        "TR_SP",
        "TR_DIA",
        "TR_CL",
        "TR_HLTH",
        "TR_CREW",
        "TR_DATE"
    ]

    # create dataframe
    prism_df = pd.DataFrame.spatial.from_featureclass(fc_prism)

    # null values allowed only when TR_SP is null (no tree) or "NoTree"
    # check TR_SP against list of accepted values

    # check for missing required fields
    missing_fields = []
    for i in rf_prism:
        if i in list(prism_df):
            pass
        else:
            missing_fields.append(i)

    # if missing fields found, list and quit
    if len(missing_fields) > 0:
        arcpy.AddError('''Field(s) {} missing from Prism points. Names must be an exact match, please check your field 
                       names and retry.'''
                       .format(missing_fields))
        sys.exit(0)

    # replace blank strings with NaN
    for i in rf_prism:
        prism_df.loc[prism_df[i] == ' ', i] = None
        prism_df.loc[prism_df[i] == '', i] = None

    # populate MIS_FIELDS with list of fields missing values
    # if TR_SP is 'NONE' or 'NoTree', check that TR_CREW and TR_DATE fields are filled out
    prism_df.loc[prism_df.TR_SP.isin(["NONE", "NoTree"]), 'MIS_FIELDS'] = prism_df[["TR_CREW",
                                                                                    "TR_DATE"]].apply(
        lambda x: ', '.join(x[x.isnull()].index), axis=1)

    arcpy.AddMessage("    MIS_FIELDS populated for no tree records")

    # if TR_SP is not 'NONE' or 'NoTree', or is null, check that all fields are filled out
    prism_df.loc[~prism_df.TR_SP.isin(["NONE", "NoTree"]), 'MIS_FIELDS'] = prism_df[["TR_SP",
                                                                                     "TR_DIA",
                                                                                     "TR_CL",
                                                                                     "TR_HLTH",
                                                                                     "TR_CREW",
                                                                                     "TR_DATE"]].apply(
        lambda x: ', '.join(x[x.isnull()].index), axis=1)

    prism_df.loc[prism_df['TR_SP'].isnull(), 'MIS_FIELDS'] = prism_df[["TR_SP",
                                                                       "TR_DIA",
                                                                       "TR_CL",
                                                                       "TR_HLTH",
                                                                       "TR_CREW",
                                                                       "TR_DATE"]].apply(
        lambda x: ', '.join(x[x.isnull()].index), axis=1)

    arcpy.AddMessage("    MIS_FIELDS populated for treed records")

    # populate HAS_MIS_FIELD
    prism_df.loc[prism_df['MIS_FIELDS'] != '', 'HAS_MIS_FIELD'] = "Yes"
    prism_df.loc[prism_df['MIS_FIELDS'] == '', 'HAS_MIS_FIELD'] = "No"

    arcpy.AddMessage("    HAS_MIS_FIELDS populated for treed records")

    # overwrite input FC
    prism_df.spatial.to_featureclass(fc_prism,
                                     overwrite=True,
                                     sanitize_columns=False)
    return fc_prism
