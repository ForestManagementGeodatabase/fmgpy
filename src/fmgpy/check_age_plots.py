import pandas as pd

def check_age_plots(age_plot_shp):
    """
    Keyword arguments:
    age_plot --

    :return:

    """

    age_df = pd.DataFrame.spatial.from_featureclass(age_plot_shp)

    field_list = list(age_df)

    if field[1] not in field_list:
        arcpy.AddError('Master Plot ID field type must be short or long integer, quitting.')
        sys.exit(0)

    return True
