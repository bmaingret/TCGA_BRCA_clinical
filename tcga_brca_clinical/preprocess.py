import pandas as pd
from typing import List
from scipy.stats import entropy


def drop_na(data: pd.DataFrame, na_cutoff: float = 1.0) -> pd.DataFrame:
    """ "Drop columns with a percentage of na values greater than
    or equal to `na_cutoff` and returns a new DataFrame"""

    case_number = data.shape[0]
    na_per_cols = data.isna().sum() / case_number
    cols_to_remove = na_per_cols[na_per_cols >= na_cutoff].index
    clean_data = data.drop(cols_to_remove, axis="columns", inplace=False)
    return clean_data


def remove_low_cardinality_features(data: pd.DataFrame) -> pd.DataFrame:
    """Remove feature with low cardinality"""
    feature_cardinality = data.select_dtypes(exclude="number").apply(
        lambda col: pd.unique(col).shape[0]
    )  # `pd.unique` includes na values
    cols_to_remove = feature_cardinality[feature_cardinality == 1].index
    return data.drop(columns=cols_to_remove)


def remove_unwanted_features(data, features: List[str]) -> pd.DataFrame:
    """Remove features from a dataframe not raising error if some features are not present.
    Useful for pipeline use."""
    return data.drop(columns=features, errors="ignore")


def categorize_features(data: pd.DataFrame) -> pd.DataFrame:
    """Change object type to category type and fill na values."""
    cat_columns = data.select_dtypes(exclude="number").columns
    data_categorized = data.copy()
    data_categorized[cat_columns] = data_categorized[cat_columns].fillna(
        value="Not Reported"
    )
    data_categorized[cat_columns] = data_categorized[cat_columns].astype(
        dtype="category"
    )
    return data_categorized


def booleanize_treatment(data: pd.DataFrame) -> pd.DataFrame:
    """Warning: Assuming  `not reported`==`no`"""
    val_dict = {"yes": True, "no": False, "not reported": False}
    data["treatment_or_therapy"] = (
        data["treatment_or_therapy"].replace(val_dict).astype(bool)
    )
    return data


def widen_treatment_type(data: pd.DataFrame) -> pd.DataFrame:
    """Transform `treatment_type`into ditsinct columns with value `treatment_or_therapy`"""
    index_cols_for_pivot = data.columns.tolist()
    index_cols_for_pivot.remove("treatment_type")
    index_cols_for_pivot.remove("treatment_or_therapy")

    wide_data = (
        data.pivot(
            index=index_cols_for_pivot,
            columns="treatment_type",
            values="treatment_or_therapy",
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    wide_data = wide_data.rename(
        columns={
            "Pharmaceutical Therapy, NOS": "pharmaceutical_therapy_nos",
            "Radiation Therapy, NOS": "radiation_therapy_nos",
        }
    )
    return wide_data


def add_treatment_feature(data: pd.DataFrame) -> pd.DataFrame:
    def treatment(row: pd.DataFrame) -> str:
        if row["pharmaceutical_therapy_nos"] and row["radiation_therapy_nos"]:
            return "both"
        if row["pharmaceutical_therapy_nos"]:
            return "pharmaceutical_therapy_nos"
        if row["radiation_therapy_nos"]:
            return "radiation_therapy_nos"
        return "no"

    data["treatment"] = data.apply(func=treatment, axis="columns")
    return data


def remove_low_entropy_features(data: pd.DataFrame, cutoff: int = 0.1) -> pd.DataFrame:
    """Remove categorical features with entropy lower than or equal to cutoff"""
    cat_features_entropy = data.select_dtypes(exclude="number").apply(
        lambda x: entropy(x.value_counts())
    )
    cols_to_drop = cat_features_entropy[cat_features_entropy <= 0.1].index
    return data.drop(columns=cols_to_drop)


def convert_to_int(data: pd.DataFrame) -> pd.DataFrame:
    """Convert float value to integer. Will raise an error if float values are not rounded numbers."""
    data_num = data.select_dtypes(include="number")
    data_converted = data.copy()
    data_converted[data_num.columns] = data_num.apply(lambda col: col.astype("Int64"))
    return data_converted


def convert_age_at_diagnosis(data: pd.DataFrame) -> pd.DataFrame:
    """Convert days to year, keeping it simple by dividing by 365.25.
    Filling-in NA values with `year_of_diagnosis` and `year_of_birth`"""
    data["age_at_diagnosis"] = (data["age_at_diagnosis"] / 365.25).astype(float)
    mask_na = data["age_at_diagnosis"].isna()
    data.loc[mask_na, "age_at_diagnosis"] = (
        data.loc[mask_na, "year_of_diagnosis"] - data.loc[mask_na, "year_of_birth"]
    )
    return data


def bin_age_at_diagnosis(data: pd.DataFrame, bins=5) -> pd.DataFrame:
    """Binning for further analysis"""
    data["age_at_diagnosis_binned"] = pd.cut(data["age_at_diagnosis"], bins=bins)
    return data


def drop_missing_death_date(data: pd.DataFrame) -> pd.DataFrame:
    rows_to_drop_query = (
        "days_to_death.isna() & year_of_death.isna() & vital_status=='Dead'"
    )
    return data.drop(index=data.query(rows_to_drop_query, engine="python").index)


def add_observed_death_feature(data: pd.DataFrame) -> pd.DataFrame:
    val_dict = {"Alive": False, "Dead": True}
    data["observed_death"] = data["vital_status"].replace(val_dict).astype(bool)
    return data


def add_survival_feature(data: pd.DataFrame) -> pd.DataFrame:
    """Build a  survival feature from `days_to_last_follow_up` and `days_to_death`.
    Feature is casted to type `float` for compatibility with `lifeline` package."""
    data["survival_days"] = data["days_to_death"]
    mask_survival = data["vital_status"] == "Alive"
    data.loc[mask_survival, "survival_days"] = data[mask_survival][
        "days_to_last_follow_up"
    ]
    data["survival_days"] = data["survival_days"].astype(float)
    return data


def preprocess_pipeline(data: pd.DataFrame) -> pd.DataFrame:
    data_prep = (
        data.pipe(drop_na)
        .pipe(remove_low_cardinality_features)
        .pipe(remove_unwanted_features, ["case_submitter_id"])
        .pipe(widen_treatment_type)
        .pipe(remove_unwanted_features, ["days_to_diagnosis"])
        .pipe(categorize_features)
        .pipe(remove_low_entropy_features)
        .pipe(convert_to_int)
        .pipe(convert_age_at_diagnosis)
        .pipe(bin_age_at_diagnosis)
        .pipe(drop_missing_death_date)
        .pipe(add_survival_feature)
        .pipe(add_observed_death_feature)
    )
    return data_prep
