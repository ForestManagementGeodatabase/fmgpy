import arcpy
import arcpy.da
import sys

def check_Plot_IDs(FC_Master, Master_PlotID_Field, FC_Check,
                   Check_PlotID_Field):
    # NEED TO CHECK MASTER FC TO ENSURE PLOT ID FIELD IS OF TYPE SHORT INTEGER
    """Checks plot id's on a given input FMG field dataset (Fixed, Prism, Age)
    based on a list of plot IDs generated from a master set of plot IDs, this
    master set of plot IDs can be the target shapefile of plot locations used
    in TerraSync, the target Plot feature class used in TerraFlex/Collector or
    the Fixed plot locations, assuming that the fixed plots have correct
    Plot IDs. The function returns the string path to the checked dataset.

    Keyword Arguments:
    FC_Master           --  The path to the feature class or table that
                            contains the full list of plot IDs, against which
                            the field data will be checked.
    Master_PlotID_Field --  The field name containing Plot IDs
    FC_Check            --  The path to the feature class or table that
                            contains the field
                            data requiring plot ID checks
    Check_PlotID_Field  --  The field name containing Plot IDs
    """

    # Check Plot ID Fields to ensure they are integer
    MasterDescribe = arcpy.Describe(FC_Master)
    for M_Field in MasterDescribe.fields:
        if M_Field.name == Master_PlotID_Field:
            if M_Field.type not in ('SmallInteger', 'Integer'):
                arcpy.AddError('Master Plot ID field type must be short or long integer, quitting.')
                sys.exit(0)

    CheckDescribe = arcpy.Describe(FC_Check)
    for C_Field in CheckDescribe.fields:
        if C_Field.name == Check_PlotID_Field:
            if C_Field.type not in ('SmallInteger', 'Integer'):
                arcpy.AddError('Check Plot ID field type must be short or long integer, quitting.')
                sys.exit(0)

    # Create a set of all valid PLOT IDs
    Plot_IDs = set([row[0] for row in arcpy.da.SearchCursor(FC_Master, Master_PlotID_Field)])

    # Add a field to the Feature Class being Checked
    FlagField = arcpy.AddField_management(in_table=FC_Check,
                                          field_name="VALID_PLOT_ID",
                                          field_type='TEXT',
                                          field_length=3)
    arcpy.AddMessage('VALID_PLOT_ID field added to '.format(FC_Check))

    # Run through the Feature Class being Checked, using new field to flag rows with Plot IDs that
    # do not match the list initially created
    with arcpy.da.UpdateCursor(FC_Check, [Check_PlotID_Field, "VALID_PLOT_ID"]) as cursor:
        for row in cursor:
            if row[0] in Plot_IDs:
                row[1] = 'Yes'
            elif row[0] not in Plot_IDs:
                row[1] = 'No'
            cursor.updateRow(row)
        del row, cursor

    arcpy.AddMessage('VALID_PLOT_ID populated, check complete')

    return FC_Check
