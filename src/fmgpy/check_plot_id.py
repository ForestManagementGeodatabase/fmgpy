# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import os
import sys
import numpy as np
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor


def check_plot_ids(fc_center, center_plot_id_field, fc_check, check_plot_id_field):
    """Checks plot IDs on a given input FMG field dataset (Fixed, Prism, Age) based on a list
    of plot IDs generated from a master set of plot IDs, this master set of plot IDs can be the
    target shapefile of plot locations used in TerraSync, the target Plot feature class used in
    TerraFlex/Collector or the Fixed plot locations, assuming that the fixed plots have correct
    Plot IDs. The function returns the string path to the checked dataset.

    Keyword Arguments:
    fc_center               --  The path to the feature class or table that contains the full list
                                of plot IDs, against which the field data will be checked.
    center_plot_id_field    --  The field name containing Plot IDs
    fc_check                --  The path to the feature class or table that contains the field
                                data requiring plot ID checks
    check_plot_id_field     --  The field name containing Plot IDs
    """

    arcpy.AddMessage(
        "Checking Plot ID fields for {0}".format(fc_center)
    )

    # create dataframes
    main_df = pd.DataFrame.spatial.from_featureclass(fc_center)
    check_df = pd.DataFrame.spatial.from_featureclass(fc_check)

    # check main plot ID field to ensure it is integer
    if main_df[center_plot_id_field].dtype == 'int64':
        arcpy.AddMessage("{0} plot ID field type is correct".format(os.path.basename(fc_center)
                                                                    ))
    else:
        arcpy.AddError(
            "{0} plot ID field type must be short or long integer, quitting.".format(os.path.basename(fc_center)
                                                                                     ))
        sys.exit(0)

    # check input plot ID field to ensure it is integer
    if check_df[check_plot_id_field].dtype == 'int64':
        arcpy.AddMessage("{0} plot ID field type is correct".format(os.path.basename(fc_check)
                                                                    ))
    else:
        arcpy.AddError(
            "(0}) plot ID field type must be short or long integer, quitting.".format(os.path.basename(fc_check))
        )
        sys.exit(0)

    # flag plot IDs not in main fc (returns boolean)
    check_df["valid_plot_id"] = check_df[check_plot_id_field].isin(main_df[center_plot_id_field])

    # convert boolean value to text Yes/No
    check_df["valid_plot_id"].apply(lambda x: np.where(x, 'Yes', 'No'))

    arcpy.AddMessage("VALID_PLOT_ID populated, check of {0} complete".format(os.path.basename(fc_check)))

    # overwrite input FC
    check_df.spatial.to_featureclass(fc_check)
    return fc_check
