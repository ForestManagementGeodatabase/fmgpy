import arcpy
import arcpy.da
import sys


def check_plot_id(fc_master, master_plot_id_field, fc_check,
                  check_plot_id_field):
    # NEED TO CHECK MASTER FC TO ENSURE PLOT ID FIELD IS OF TYPE SHORT INTEGER
    """Checks plot IDs on a given input FMG field dataset (Fixed, Prism, Age)
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
    master_describe = arcpy.Describe(fc_master)
    for M_Field in master_describe.fields:
        if M_Field.name == master_plot_id_field:
            if M_Field.type not in ('SmallInteger', 'Integer'):
                arcpy.AddError('Master Plot ID field type must be short or long integer, quitting.')
                sys.exit(0)

    check_describe = arcpy.Describe(fc_check)
    for C_Field in check_describe.fields:
        if C_Field.name == check_plot_id_field:
            if C_Field.type not in ('SmallInteger', 'Integer'):
                arcpy.AddError('Check Plot ID field type must be short or long integer, quitting.')
                sys.exit(0)

    # Create a set of all valid PLOT IDs
    Plot_IDs = set([row[0] for row in arcpy.da.SearchCursor(fc_master, master_plot_id_field)])

    # Add a field to the Feature Class being Checked
    flag_field = arcpy.AddField_management(in_table=fc_check,
                                           field_name="VALID_PLOT_ID",
                                           field_type='TEXT',
                                           field_length=3)
    arcpy.AddMessage('VALID_PLOT_ID field added to '.format(fc_check))

    # Run through the Feature Class being Checked, using new field to flag rows with Plot IDs that
    # do not match the list initially created
    with arcpy.da.UpdateCursor(fc_check, [check_plot_id_field, "VALID_PLOT_ID"]) as cursor:
        for row in cursor:
            if row[0] in Plot_IDs:
                row[1] = 'Yes'
            elif row[0] not in Plot_IDs:
                row[1] = 'No'
            cursor.updateRow(row)
        del row, cursor

    arcpy.AddMessage('VALID_PLOT_ID populated, check complete')

    return fc_check
