# %%
import pandas as pd
import html

# %%


def parse(path):
    with open(path, "r") as f:
        for line in f:
            yield eval(line)


# %%
filename = "ratebeer.json"
df_raw = pd.DataFrame.from_records(parse(filename), nrows=100000)
df_raw.columns = df_raw.columns.str.replace("/", "_")

# %%
df_raw.info()

# %%
pd.options.plotting.backend = "plotly"

# %%


def clean_integer_features(df, columns):
    df = df.copy()
    for c in columns:
        df[c] = df[c].str.split("/").str[0].astype(int)
    return df


def clean_float_features(df, columns):
    df = df.copy()
    for c in columns:
        df[c] = df[c].replace("-", -1).astype(float)
    return df


def clean_categorical_features(df, columns):
    df = df.copy()
    for c in columns:
        df[c] = df[c].apply(html.unescape)
    return df


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

df = (
    (df_raw)
    .pipe(clean_integer_features, integer_features)
    .pipe(clean_float_features, float_features)
    .pipe(clean_categorical_features, categorical_features)
)
df

# %%
from scipy.stats import chi2_contingency
print(chi2_contingency(pd.crosstab(df.beer_style, df.review_overall))[1])
pd.crosstab(df.beer_style, df.review_overall).plot(kind="imshow")

# %%
(
    df
    .assign(review_overall=lambda df: df.review_overall.pipe(lambda s: s - s.mean()))
    .groupby("beer_style", as_index=False)
    .review_overall.agg(["mean", "std", "count"])
    .add_prefix("review_overall_")
    .style.background_gradient(cmap="RdYlBu")
)

# %% [markdown]
# 1. continuous features:
#     1. preprocessing
#         - scaling
#         - transformation
#     1. plot:
#         - scatter (continuous target)
#         - histogram / kde (categorical target)
#     1. stat test:
# 1. categorical features:
#     1. preprocessing
#         - label encoding
#         - one-hot encoding
#         - target encoding
#     1. plot:
#         - ...
#     1. stat test: 
#         - ...
# 


# %% [markdown]
# Variable types:
# | Data Type | Shorthand Code | Description |
# | --- | --- | --- |
# | quantitative | Q | a continuous real-valued quantity |
# | ordinal | O | a discrete ordered quantity |
# | nominal | N | a discrete unordered category |
# | temporal | T | a time or date value |
# | geojson | G | a geographic shape |
#
# | Data type | Object | Feature type |
# |---|---|
# | Numerical / Continuous | float | Ratio |
# | Numerical / Continuous | float | Interval |
# | Categorical / Discrete | string / int | Nominal |
# | Categorical / Discrete | int | Ordinal |

# Complex data type:
# | Array[Numerical] |  |
# | Array[Numerical] |  |


# %% [markdown]
# |   | Quantitative | Ordinal |
# |---|---|---|
# |  a | a  | a  |
# |  a |   a|  a |
