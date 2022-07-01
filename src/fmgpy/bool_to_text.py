# -*- coding: UTF-8 -*-
# FMG QA Tools Function Library

import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor


def yes_no(df_name, field_name):
    df_name.loc[df_name[field_name] == 1, field_name] = "Yes"
    df_name.loc[df_name[field_name] == 0, field_name] = "No"
