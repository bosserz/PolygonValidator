# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# import all necessary libs
import geopandas as gpd
import pandas as pd
from sys import argv, exit

col_names = ["id", "name", "category", "sub_category"]

def check_column_name(gdf):

    result = []

    for col in col_names:

        if col not in gdf.columns:

            result.append("File does not have column " + col)

    return result

def check_duplicates(gdf, col):

    """
    :param gdf:
    :param col:
    :return:
        value which causing duplication
    """
    if len(gdf[gdf.duplicated(subset = col)]) > 0:

        dup_gdf = gdf[gdf.duplicated(subset = col, keep = False)]
        return (True, dup_gdf, dup_gdf[col].nunique())

    return (False, None, 0)

def check_category(gdf):

    if gdf.category.nunique() > 1:

        return False

    else:

        return True

def validator(filename):

    gdf = gpd.read_file(filename)

    filename_no_ending = filename.split(".")[0]

    results = []

    # check columns name
    results += check_column_name(gdf)

    # check id duplicate
    check_id, duplicates_id, len_dup_id = check_duplicates(gdf, "id")

    if check_id:
        results.append(f"there are {len_dup_id} duplicated id")
        duplicates_id.to_file(f"{filename_no_ending}_duplicate_id.geojson", driver="GeoJSON")

    # check name duplicates
    check_name, duplicates_name, len_dup_name = check_duplicates(gdf, "name")

    if check_name:
        results.append(f"there are {len_dup_name} duplicated name")
        duplicates_name.to_file(f"{filename_no_ending}_duplicates_name.geojson", driver="GeoJSON")

    for error in results:
        print(error)

    return 0
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print("load polygon file...")

    if len(argv) != 2:

        print("Usage python main.py file_name.geojson")

        exit(1)
    if argv[1].split(".")[-1] != "geojson":

        print("Only 'geojson' is supported for current version.")

        exit(1)

    validator(argv[1])

    exit(0)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
