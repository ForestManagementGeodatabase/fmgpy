# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import arcpy
import os, sys
import numpy as np
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

arcpy.env.overwriteOutput = True


def check_Plot_IDs(FC_Center, Center_PlotID_Field, FC_Check, Check_PlotID_Field):
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
        "Checking Plot ID fields for {0}".format(FC_Center)
    )

    # create dataframes
    center_df = pd.DataFrame.spatial.from_featureclass(FC_Center)
    check_df = pd.DataFrame.spatial.from_featureclass(FC_Check)

    # check main plot ID field to ensure it is integer
    if center_df[Center_PlotID_Field].dtype == 'int64':
        arcpy.AddMessage("{0} plot ID field type is correct".format(os.path.basename(FC_Center)
                                                                    ))
    else:
        arcpy.AddError(
            "{0} plot ID field type must be short or long integer, quitting.".format(os.path.basename(FC_Center)
                                                                                     ))
        sys.exit(0)

    # check input plot ID field to ensure it is integer
    if check_df[Check_PlotID_Field].dtype == 'int64':
        arcpy.AddMessage("{0} plot ID field type is correct".format(os.path.basename(FC_Check)
                                                                    ))
    else:
        arcpy.AddError(
            "(0}) plot ID field type must be short or long integer, quitting.".format(os.path.basename(FC_Check))
        )
        sys.exit(0)

    # flag plot IDs not in main fc (returns boolean)
    check_df["valid_plot_id"] = check_df[Check_PlotID_Field].isin(center_df[Center_PlotID_Field])

    # convert boolean value to text Yes/No
    check_df["valid_plot_id"].apply(lambda x: np.where(x, 'Yes', 'No'))

    arcpy.AddMessage("VALID_PLOT_ID populated, check of {0} complete".format(os.path.basename(FC_Check)))

    # overwrite input FC
    check_df.spatial.to_featureclass(FC_Check)
    return FC_Check


def check_Fixed_Offset(FC_PlotLocations, PlotID_Field, FC_Fixed, Fixed_PlotID_Field):
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
    plot_df = pd.DataFrame.spatial.from_featureclass(FC_PlotLocations)
    fixed_df = pd.DataFrame.spatial.from_featureclass(FC_Fixed)

    # calculate horizontal offset between fixed points and main plot center
    # join plot center SHAPE field to fixed on plot ID
    fixed_coords = fixed_df.join(plot_df[[PlotID_Field, 'SHAPE']].set_index(PlotID_Field),
                                 on=Fixed_PlotID_Field,
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
    fixed_df.spatial.to_featureclass(FC_Fixed)
    return FC_Fixed


def check_Prism_Fixed(FC_Prism, Prism_PlotID, FC_Fixed, Fixed_PlotID):
    """ Checks to make sure there is a prism plot for every fixed plot and that there is a
    fixed plot for each prism plot. This is accomplished by comparing unique sets of plot
    IDs present for each feature class and populating fields indicating if this relationship
    holds true

    Keyword Arguments:
    FC_Prism      -- Path to prism feature class
    Prism_PlotID  -- Prism feature class plot ID field
    FC_Fixed      -- Path to fixed plot feature class
    Fixed_PlotID  -- Fixed feature class plot ID field
    """

    arcpy.AddMessage(
        "Checking for existence of corresponding prism and fixed plots"
    )

    # create dataframes
    prism_df = pd.DataFrame.spatial.from_featureclass(FC_Prism)
    fixed_df = pd.DataFrame.spatial.from_featureclass(FC_Fixed)

    # flag prism plot IDs without corresponding fixed plot
    prism_df["has_fixed"] = prism_df[Prism_PlotID].isin(fixed_df[Fixed_PlotID])
    arcpy.AddMessage(
        "Prism points {0} checked for corresponding fixed points".format(FC_Prism)
    )
    # convert boolean value to text Yes/No
    prism_df["has_fixed"].apply(lambda x: np.where(x, 'Yes', 'No'))

    # flag fixed plot IDs without corresponding prism plot
    fixed_df["has_prism"] = fixed_df[Fixed_PlotID].isin(prism_df[Prism_PlotID])
    arcpy.AddMessage(
        "Fixed points {0} checked for corresponding prism points".format(FC_Fixed)
    )
    # convert boolean value to text Yes/No
    fixed_df["has_prism"].apply(lambda x: np.where(x, 'Yes', 'No'))

    # overwrite input FC
    prism_df.spatial.to_featureclass(FC_Prism)
    fixed_df.spatial.to_featureclass(FC_Fixed)
    return [FC_Prism, FC_Fixed]


def check_Contractor_Age_Plots(FC_Plots, Plots_PlotID, Age_FlagField, FC_Age, Age_PlotID):
    """Checks prescribed age plots against collected age plots. Returns the prescribed age
    plots with a flag field indicating if an age plot was collected.

    Keyword Arguments:
    FC_Plots       --  Path to feature class of required plot locations
    Plots_PlotID   --  Field name of Plot ID column for required plot location feature class
    Age_FlagField  --  Field name of age requirement flag field for required plot location feature class
    FC_Age         --  Path to feature class of contractor submitted age plots
    Age_PlotID     --  Field name of Plot ID column for contractor submitted age plot feature class
    """

    # Check to ensure Age plots exit where required, adding and populating a flag field on the Plot feature class

    # Create dataframes
    plots_df = pd.DataFrame.spatial.from_featureclass(FC_Plots)
    age_df = pd.DataFrame.spatial.from_featureclass(FC_Age)

    # Create sets of Plots ID for collected age plots

    Required_Age_PlotIDs = set(
        [row[0] for row in arcpy.da.SearchCursor(
            FC_Plots, Plots_PlotID, "{0} = 'A'".format(Age_FlagField)
        )]
    )

    # where age_FlagField = A in inPlot
    plots_df["HAS_AGE"] = plots_df[Plots_PlotID].isin(age_df[Age_PlotID])
    arcpy.AddMessage("Plot points checked for corresponding age record")

    # TODO: save out dataframes
    # overwrite input FC
    return FC_Plots


def check_Required_Fields_Prism(FC_Prism):
    arcpy.AddMessage("Begin check on Prism points")

    # List of required fields
    RF_Prism = [
        "TR_SP",
        "TR_DIA",
        "TR_CL",
        "TR_HLTH",
        "TR_CREW",
        "TR_DATE",
        "HAS_MIS_FIELD",
        "MIS_FIELD",
    ]

    # Add check fields to input feature classes
    arcpy.AddField_management(
        in_table=FC_Prism, field_name="HAS_MIS_FIELD", field_type="TEXT", field_length=5
    )
    arcpy.AddField_management(
        in_table=FC_Prism, field_name="MIS_FIELD", field_type="TEXT", field_length=80
    )
    arcpy.AddMessage("    Fields added to {0}".format(FC_Prism))

    # Populate HAS_MIS_FIELD if null values exist in required fields where TR_SP = NONE
    row_count = len(
        list(i for i in arcpy.da.SearchCursor(FC_Prism, RF_Prism, "TR_SP = 'NONE'"))
    )
    if row_count == 0:
        arcpy.AddMessage("    No records found where TR_SP = NONE")
    elif row_count != 0:
        with arcpy.da.UpdateCursor(FC_Prism, RF_Prism, "TR_SP = 'NONE'") as cursor:
            for row in cursor:
                if None in row[4:6]:
                    row[6] = "Yes"
                elif None not in row[4:6]:
                    row[6] = "No"
                cursor.updateRow(row)
            del row, cursor
        arcpy.AddMessage("    HAS_MIS_FIELD populated for no tree records")

    # Populate HAS_MIS_FIELD if null values exist in required fields for all other records
    row_count = len(
        list(
            i
            for i in arcpy.da.SearchCursor(
                FC_Prism, RF_Prism, "TR_SP <> 'NONE' OR TR_SP IS NULL"
            )
        )
    )
    if row_count == 0:
        arcpy.AddMessage("No records contain tree species")
    elif row_count != 0:
        with arcpy.da.UpdateCursor(
                FC_Prism, RF_Prism, "TR_SP <> 'NONE' OR TR_SP IS NULL"
        ) as cursor:
            for row in cursor:
                if None in row[0:6]:
                    row[6] = "Yes"
                elif None not in row[0:6]:
                    row[6] = "No"
                cursor.updateRow(row)
            del row, cursor
        arcpy.AddMessage("    HAS_MIS_FIELD populated for treed records")

    # Check to ensure rows exist with tree species type 'NONE' and missing fields, then populate MIS_FIELD with missing field names
    arcpy.MakeQueryTable_management(
        in_table=FC_Prism,
        out_table="Q_Table",
        in_key_field_option="NO_KEY_FIELD",
        where_clause="HAS_MIS_FIELD = 'Yes' AND TR_SP = 'NONE'",
    )  # Query validated
    QueryRows = int(arcpy.GetCount_management("Q_Table").getOutput(0))
    arcpy.Delete_management("Q_Table")
    if QueryRows != 0:
        with arcpy.da.UpdateCursor(
                FC_Prism, RF_Prism, "HAS_MIS_FIELD = 'Yes' AND TR_SP = 'NONE'"
        ) as cursor:
            for row in cursor:
                MissingFields = []
                if row[4] is None:
                    MissingFields.append(RF_Prism[4])
                elif row[5] is None:
                    MissingFields.append(RF_Prism[5])
                row[7] = ", ".join(map(str, MissingFields))
                cursor.updateRow(row)
                MissingFields = []
            del row, cursor
    arcpy.AddMessage("    MIS_FIELDS populated for no tree records")

    # Populate MIS_FIELDS with missing field names for all other cases
    arcpy.MakeQueryTable_management(
        in_table=FC_Prism,
        out_table="Q_Table",
        in_key_field_option="NO_KEY_FIELD",
        where_clause="HAS_MIS_FIELD = 'Yes' AND TR_SP <> 'NONE' OR TR_SP IS NULL",
    )
    QueryRows = int(arcpy.GetCount_management("Q_Table").getOutput(0))
    arcpy.Delete_management("Q_Table")
    if QueryRows != 0:
        with arcpy.da.UpdateCursor(
                FC_Prism,
                RF_Prism,
                "HAS_MIS_FIELD = 'Yes' AND TR_SP <> 'NONE' OR TR_SP IS NULL",
        ) as cursor:
            for row in cursor:
                MissingFields = []
                for i in range(0, len(row[2:])):
                    if row[i] is None:
                        MissingFields.append(RF_Prism[i])
                row[7] = ", ".join(map(str, MissingFields))
                cursor.updateRow(row)
                MissingFields = []
            del row, cursor
    arcpy.AddMessage("    MIS_FIELDS populated for treed records")

    # TODO: save out dataframes
    # overwrite input FC
    return FC_Prism


def check_Required_Fields_Age(FC_Age):
    arcpy.AddMessage("Begin check on Age points")

    # List of required fields
    RF_Age = [
        "AGE_SP",
        "AGE_DIA",
        "AGE_HT",
        "AGE_ORIG",
        "AGE_GRW",
        "AGE_CREW",
        "AGE_DATE",
        "HAS_MIS_FIELD",
        "MIS_FIELD",
    ]

    # Add check fields to input feature classes
    arcpy.AddField_management(
        in_table=FC_Age, field_name="HAS_MIS_FIELD", field_type="TEXT", field_length=5
    )
    arcpy.AddField_management(
        in_table=FC_Age, field_name="MIS_FIELD", field_type="TEXT", field_length=80
    )
    arcpy.AddMessage("    Fields added to {0}".format(FC_Age))

    # Populate HAS_MIS_FIELD
    with arcpy.da.UpdateCursor(FC_Age, RF_Age) as cursor:
        for row in cursor:
            if None in row[0:7]:
                row[7] = "Yes"
            elif None not in row[0:7]:
                row[7] = "No"
            cursor.updateRow(row)
        del row, cursor
    arcpy.AddMessage("    HAS_MIS_FIELD populated")

    # Populate MIS_FIELDS with missing field names for all other cases
    arcpy.MakeQueryTable_management(
        in_table=FC_Age,
        out_table="Q_Table",
        in_key_field_option="NO_KEY_FIELD",
        where_clause="HAS_MIS_FIELD = 'Yes'",
    )
    QueryRows = int(arcpy.GetCount_management("Q_Table").getOutput(0))
    arcpy.Delete_management("Q_Table")
    if QueryRows != 0:
        with arcpy.da.UpdateCursor(FC_Age, RF_Age, "HAS_MIS_FIELD = 'Yes'") as cursor:
            for row in cursor:
                MissingFields = []
                for i in range(0, len(row[2:])):
                    if row[i] is None:
                        MissingFields.append(RF_Age[i])
                row[8] = ", ".join(map(str, MissingFields))
                cursor.updateRow(row)
                MissingFields = []
            del row, cursor
    arcpy.AddMessage("    MIS_FIELDS populated")

    # TODO: save out dataframes
    # overwrite input FC

    return FC_Age


def check_Required_Fields_Fixed(FC_Fixed):
    arcpy.AddMessage("Begin check on Fixed plots")

    # List of required fields
    RF_Fixed = [
        "OV_CLSR",
        "OV_HT",
        "UND_HT",
        "UND_COV",
        "UND_SP1",
        "GRD_SP1",
        "FP_CREW",
        "FP_DATE",
        "HAS_MIS_FIELD",
        "MIS_FIELD",
    ]

    # Add check fields to input feature classes
    arcpy.AddField_management(
        in_table=FC_Fixed, field_name="HAS_MIS_FIELD", field_type="TEXT", field_length=5
    )
    arcpy.AddField_management(
        in_table=FC_Fixed, field_name="MIS_FIELD", field_type="TEXT", field_length=80
    )
    arcpy.AddMessage("    Fields added to {0}".format(FC_Fixed))

    # Populate HAS_MIS_FIELD
    with arcpy.da.UpdateCursor(FC_Fixed, RF_Fixed) as cursor:
        for row in cursor:
            if None in row[0:8]:
                row[8] = "Yes"
            elif None not in row[0:8]:
                row[8] = "No"
            cursor.updateRow(row)
        del row, cursor
    arcpy.AddMessage("    HAS_MIS_FIELD populated")

    # Populate MIS_FIELDS with missing field names for all other cases
    arcpy.MakeQueryTable_management(
        in_table=FC_Fixed,
        out_table="Q_Table",
        in_key_field_option="NO_KEY_FIELD",
        where_clause="HAS_MIS_FIELD = 'Yes'",
    )
    QueryRows = int(arcpy.GetCount_management("Q_Table").getOutput(0))
    arcpy.Delete_management("Q_Table")
    if QueryRows != 0:
        with arcpy.da.UpdateCursor(
                FC_Fixed, RF_Fixed, "HAS_MIS_FIELD = 'Yes'"
        ) as cursor:
            for row in cursor:
                MissingFields = []
                for i in range(0, len(row[2:])):
                    if row[i] is None:
                        MissingFields.append(RF_Fixed[i])
                row[9] = ", ".join(map(str, MissingFields))
                cursor.updateRow(row)
                MissingFields = []
            del row, cursor
    arcpy.AddMessage("    MIS_FIELDS populated")

    # TODO: save out dataframes
    # overwrite input FC

    return FC_Fixed
