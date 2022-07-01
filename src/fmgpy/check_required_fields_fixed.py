# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import sys
import pandas as pd
import numpy as np

from arcgis.features import GeoAccessor, GeoSeriesAccessor

arcpy.env.overwriteOutput = True


def check_required_fields_fixed(fc_fixed):
    """Checks fixed plots for presence of required fields and for missing values in those fields.

    Keyword Arguments:
    fc_fixed    -- Path to fixed feature class
    """

    arcpy.AddMessage("Begin check on Fixed plots")

    # list of required fields
    rf_fixed = [
        "OV_CLSR",
        "OV_HT",
        "UND_HT",
        "UND_COV",
        "UND_SP1",
        "GRD_SP1",
        "FP_CREW",
        "FP_DATE"
    ]

    # create dataframe
    fixed_df = pd.DataFrame.spatial.from_featureclass(fc_fixed)

    # check for missing required fields
    missing_fields = []
    for i in rf_fixed:
        if i in list(fixed_df):
            pass
        else:
            missing_fields.append(i)

    # if missing fields found, list and quit
    if len(missing_fields) > 0:
        arcpy.AddError('''Field(s) {} missing from Fixed points. Names must be an exact match, please check your field 
                       names and retry.'''
                       .format(missing_fields))
        sys.exit(0)

    # replace blank strings with NaN
    for i in rf_fixed:
        fixed_df.loc[fixed_df[i] == ' ', i] = None
        fixed_df.loc[fixed_df[i] == '', i] = None

    # populate MIS_FIELDS with list of fields missing values
    fixed_df['MIS_FIELDS'] = fixed_df[["OV_CLSR",
                                       "OV_HT",
                                       "UND_HT",
                                       "UND_COV",
                                       "UND_SP1",
                                       "GRD_SP1",
                                       "FP_CREW",
                                       "FP_DATE"]].apply(
        lambda x: ', '.join(x[x.isnull()].index), axis=1)

    arcpy.AddMessage("    MIS_FIELDS populated")

    # populate HAS_MIS_FIELD
    fixed_df.loc[fixed_df['MIS_FIELDS'] != '', 'HAS_MIS_FIELD'] = "Yes"
    fixed_df.loc[fixed_df['MIS_FIELDS'] == '', 'HAS_MIS_FIELD'] = "No"

    arcpy.AddMessage("    HAS_MIS_FIELDS populated")

    # overwrite input FC
    fixed_df.spatial.to_featureclass(fc_fixed,
                                     overwrite=True,
                                     sanitize_columns=False)

    return fc_fixed
