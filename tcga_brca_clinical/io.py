import pandas as pd


def save_data(data: pd.DataFrame, path: str) -> None:
    data.to_pickle(path)


def read_data(path: str) -> pd.DataFrame:
    return pd.read_pickle(path)


def read_raw_data(path: str):
    data = pd.read_table(filepath_or_buffer=path, sep="\t", na_values=["'--"])
    return data
