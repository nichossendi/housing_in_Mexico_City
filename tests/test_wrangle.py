import pandas as pd
import pytest

from housing.wrangle import wrangle

SAMPLE_FILE = "data/mexico_city_real_estate_1.csv"


@pytest.fixture
def df():
    return wrangle(SAMPLE_FILE)


def test_only_apartments_under_100k(df):
    assert (df["property_type"] == "apartment").all(), "Dataframe contains non-apartment property types"
    assert df["price_aprox_usd"].max() < 100_000, "Dataframe contains apartments priced over $100,000"
    assert (df["price_aprox_usd"] > 0).all(), "Dataframe contains apartments with non-positive prices"


def test_surface_area_outliers(df):
    raw = pd.read_csv(SAMPLE_FILE)
    subset = raw[
        raw["place_with_parent_names"].str.contains("Distrito Federal")
        & (raw["property_type"] == "apartment")
        & (raw["price_aprox_usd"] < 100_000)
    ]
    low, high = subset["surface_covered_in_m2"].quantile([0.1, 0.9])
    assert df["surface_covered_in_m2"].between(low, high).all(), (
        "Dataframe contains apartments with surface areas outside the 10th and 90th percentiles"
    )


def test_borough_column(df):
    assert "borough" in df.columns, "Dataframe does not contain a 'borough' column"
    assert df["borough"].notnull().all(), "Dataframe contains null values in the 'borough' column"


def test_lat_lon_columns(df):
    assert "lat" in df.columns, "Dataframe does not contain a 'lat' column"
    assert "lon" in df.columns, "Dataframe does not contain a 'lon' column"
    assert df["lat"].dtype == float, "'lat' column is not of type float"
    assert df["lon"].dtype == float, "'lon' column is not of type float"


def test_dropped_columns(df):
    dropped_columns = [
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
        "properati_url",
    ]
    for col in dropped_columns:
        assert col not in df.columns, f"Dataframe still contains the '{col}' column"