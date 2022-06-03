import os
import pandas as pd

from arcgis.features import GeoAccessor, GeoSeriesAccessor

test_folder = os.path.relpath("./data/Pool_17_20210930")

test_folder_path = os.path.realpath(test_folder)

age_path = os.path.join(test_folder_path, "Age.shp")

age_df = pd.DataFrame.spatial.from_featureclass(age_path)

field_list = list(age_df)

# print(age_df['AGE_ORIG'])
years = age_df['AGE_ORIG']

field = 'AGE_ORIG'

ages = age_df[field].tolist()
print(age_df[[field, "AGE_SP"]])

for row in age_df[[field, "AGE_SP"]].itertuples(name='plots'):
    if row[1] == 0:
        print(age_df.at[row.Index, "AGE_SP"])

# for index, value in age_df['AGE_ORIG'].items():
#     print(len(str(value)))


# def test_age_fields():
#     assert "AGE_ORIG" in list(age_df)
#
#
# def test_age_orig():
#     for index, value in age_df['AGE_ORIG'].items():
#         if value < 1000:
#             assert value is None
#         elif value > 1000:
#             assert len(str(value)) == 4
