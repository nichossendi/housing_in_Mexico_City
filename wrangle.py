import pandas as pd

def wrangle(filepath):
    
    """
    This function imports a csv file into a pandas dataframe,
    subsets the dataframe to include only Distrito Federal apartments under $100,000,
    and trims outlier surface areas,
    returning the cleaned dataframe,
    which includes a new "borough" column created from the "place_with_parent_names" column,
    and new "lat" and "lon" columns created from the "lat-lon" column,
    while dropping irrelevant and redundant columns
    and resetting the index of the dataframe.
    """

    # Import csv file into a dataframe
    df = pd.read_csv(filepath)

    # Subset to include only Distrito Federal apartments under $100,000
    mask_df = df["place_with_parent_names"].str.contains("Distrito Federal")
    mask_ap = df["property_type"] == "apartment"
    mask_price = df["price_aprox_usd"] < 100000
    df = df[mask_df & mask_ap & mask_price]

    # Trimming outlier surface areas
    low, high = df["surface_covered_in_m2"].quantile([0.1, 0.9])
    mask_area = df["surface_covered_in_m2"].between(low, high)
    df = df[mask_area]

    # Creating the "borough" column from "place_with_parent_names"
    df["borough"] = df["place_with_parent_names"].str.split("|", expand = True)[3]

    # Creating the "lat" column from "lat-lon"
    df["lat"] = df["lat-lon"].str.split(",", expand = True)[0].astype(float)

    # Creating the "lon" column from "lat-lon"
    df["lon"] = df["lat-lon"].str.split(",", expand = True)[1].astype(float)

    # Dropping irrelevant and redundant columns
    df.drop(columns = [
        "place_with_parent_names",
        "operation",
        "currency",
        "price",
        "price_aprox_local_currency",
        "surface_total_in_m2",
        "price_usd_per_m2",
        "price_per_m2",
        "floor",
        "rooms",
        "expenses",
        "lat-lon",
        "properati_url"
        ], inplace = True)
    
    # Resetting the index of the dataframe
    df.reset_index(drop = True, inplace = True)

    return df