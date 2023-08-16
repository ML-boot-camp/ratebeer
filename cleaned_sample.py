import pandas as pd

from utils import (
    parse, 
    clean_column_names,
    clean_integer_features,
    clean_float_features,
    clean_categorical_features
)

def main():
    """
    Generate a clean sample of the raw ratebeer json file.
    The sample is saved as parquet file.
    """

    data_dir = "data/"
    raw_filename = "ratebeer.json" 
    N_rows = 200000 

    # Load the data and select a sample
    df_raw = (
        pd.DataFrame.from_records(parse(data_dir+raw_filename))
        .sample(n=N_rows, random_state=42)
    )

    # Define column types
    integer_features = [
        "review_appearance",
        "review_aroma",
        "review_palate",
        "review_taste",
        "review_overall",
    ]

    float_features = [
        "beer_ABV",
    ]

    categorical_features = [
        "beer_name",
        "beer_style",
    ]

    # Rename columns
    rename_dict = {
        "beer_name": "beer",
        "beer_brewerId": "brewery",
        "beer_ABV": "alcohol",
        "beer_style": "type",
        "review_appearance": "rating_appearance",
        "review_aroma": "rating_aroma",
        "review_palate": "rating_palate",
        "review_taste": "rating_taste",
        "review_overall": "rating",
        "review_time": "time",
        "review_profileName": "user",
        "review_text": "text",
    }

    # Apply cleaning steps to the data
    df_clean = (
        (df_raw)
        .pipe(clean_column_names)
        .pipe(clean_integer_features, integer_features)
        .pipe(clean_float_features, float_features)
        .pipe(clean_categorical_features, categorical_features)
        .drop("beer_beerId", axis=1)
        .rename(columns=rename_dict)
    )

    # Save the cleaned sample of data
    clean_filename = "ratebeer_sample_clean.parquet"
    df_clean.to_parquet(data_dir + clean_filename)


if __name__ == "__main__":
    main()
