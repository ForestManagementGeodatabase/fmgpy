# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import sys
import pandas as pd
import numpy as np

from arcgis.features import GeoAccessor, GeoSeriesAccessor

arcpy.env.overwriteOutput = True


def check_required_fields_age(fc_age):
    arcpy.AddMessage("Begin check on Age points")

    # List of required fields
    rf_age = [
        "AGE_SP",
        "AGE_DIA",
        "AGE_HT",
        "AGE_ORIG",
        "AGE_GRW",
        "AGE_CREW",
        "AGE_DATE"
    ]

    # create dataframe
    age_df = pd.DataFrame.spatial.from_featureclass(fc_age)

    # check for missing required fields
    missing_fields = []
    for i in rf_age:
        if i in list(age_df):
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
    for i in rf_age:
        age_df.loc[age_df[i] == ' ', i] = np.nan
        age_df.loc[age_df[i] == '', i] = np.nan

    # populate MIS_FIELDS with list of fields missing values
    age_df['MIS_FIELDS'] = age_df[["AGE_SP",
                                   "AGE_DIA",
                                   "AGE_HT",
                                   "AGE_ORIG",
                                   "AGE_GRW",
                                   "AGE_CREW",
                                   "AGE_DATE"]].apply(
        lambda x: ','.join(x[x.isnull()].index), axis=1)

    arcpy.AddMessage("    MIS_FIELDS populated")

    # Populate HAS_MIS_FIELD
    age_df.loc[age_df['MIS_FIELDS'] != '', 'HAS_MIS_FIELD'] = "Yes"
    age_df.loc[age_df['MIS_FIELDS'] == '', 'HAS_MIS_FIELD'] = "No"

    arcpy.AddMessage("    HAS_MIS_FIELDS populated")

    # overwrite input FC
    age_df.spatial.to_featureclass(fc_age,
                                   overwrite=True,
                                   sanitize_columns=False)

    return fc_age
