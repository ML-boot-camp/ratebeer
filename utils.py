import pandas as pd
import html

def parse(path):
    with open(path, "r") as f:
        for line in f:
            yield eval(line)


def clean_column_names(df):
    df.columns = df.columns.str.replace("/", "_")
    return df


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