# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import numpy as np
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

arcpy.env.overwriteOutput = True


def check_fixed_offset(fc_center, center_plot_id_field, fc_fixed, fixed_plot_id_field):
    """Checks the location of fixed plots against the initial set of target plots by creating
    a new field on the fixed plot dataset and populating it with the distance it is from the
    target plot location. This distance should be in meters, which means both input feature
    classes must have a coordinate system in meters.

    Keyword Arguments:
    FC_PlotLocations    --  The path to the feature class containing the target plot locations
    PlotID_Field        --  The field name containing Plot IDs of the target plot locations
    FC_Fixed            --  The path to the feature class containing fixed plot locations
    Fixed_PlotID_Field  --  The field name containing Plot IDs of the fixed plot locations
    """
    arcpy.AddMessage(
        "Calculating horizontal offset between fixed plots and plot centers"
    )

    # create dataframes
    center_df = pd.DataFrame.spatial.from_featureclass(fc_center)
    fixed_df = pd.DataFrame.spatial.from_featureclass(fc_fixed)

    # calculate horizontal offset between fixed points and main plot center
    # join plot center SHAPE field to fixed on plot ID
    fixed_coords = fixed_df.join(center_df[[center_plot_id_field, 'SHAPE']].set_index(center_plot_id_field),
                                 on=fixed_plot_id_field,
                                 lsuffix='_fixed',
                                 rsuffix='_plot')

    fixed_coords['FIXED_X'] = fixed_coords['SHAPE_fixed'].apply(lambda x: x.get('x'))
    fixed_coords['FIXED_Y'] = fixed_coords['SHAPE_fixed'].apply(lambda x: x.get('y'))
    fixed_coords['PLOT_X'] = fixed_coords['SHAPE_plot'].apply(lambda x: x.get('x'))
    fixed_coords['PLOT_Y'] = fixed_coords['SHAPE_plot'].apply(lambda x: x.get('y'))

    # calc difference in x
    dx = fixed_coords['PLOT_X'] - fixed_coords['FIXED_X']
    # calc difference in y
    dy = fixed_coords['PLOT_Y'] - fixed_coords['FIXED_Y']
    # calc offset [sq rt (dx^2 + dy^2)] and write to new column
    fixed_coords["DIST_FROM_TARGET_M"] = np.sqrt((dx ** 2) + (dy ** 2))
    fixed_df["DIST_FROM_TARGET_M"] = np.sqrt((dx ** 2) + (dy ** 2))

    arcpy.AddMessage("Offsets calculated")

    # overwrite input FC
    fixed_df.spatial.to_featureclass(fc_fixed, sanitize_columns=False)
    return fc_fixed
