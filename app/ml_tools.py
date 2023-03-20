"""This module contains all that is needed to preform model tasks."""
import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

logger = logging.getLogger("ml-tools")


def load_data() -> pd.DataFrame:
    """Reads the base features working file"""
    try:
        return pd.read_csv("data/features.csv", index_col="index")
    except FileNotFoundError as error:
        logger.error("Cannot read features file, ERROR %s: ", error)
        raise


def prepare_train_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Prepares data for training the model."""
    train = data[data["TARGET"].notnull()].copy()
    labels = train["TARGET"].copy()

    train.drop(["SK_ID_CURR", "TARGET"], axis=1, inplace=True)
    train.replace([np.inf, -np.inf], np.nan, inplace=True)

    imp = SimpleImputer(missing_values=np.nan, strategy="median")
    imp.set_output(transform="pandas")
    imp.fit_transform(train)

    return train, labels


def prepare_predict_data(data: dict) -> dict:
    """Prepares the input dict to be used in prediction"""
    # TODO: The input dictionary will contain unecessary columns that have to be
    #   stripped away to be able to use it. Add the dictionary cleanin here and
    #   return a clean dictionary.
    return data


def train_model(data, target) -> RandomForestClassifier:
    """Trains a random forest model and returns it for further operations"""
    random_forest = RandomForestClassifier(n_estimators=5, random_state=150, n_jobs=-1)
    random_forest.fit(data, target)

    return random_forest


def append_new_customer(customer: dict):
    """Appends the new customer to the existing dataset.
    The dictionary must have all the columns of the dataset.
    """
    data = load_data()
    data.append(customer, ignore_index=True)
    data.to_csv("data/features.csv")


def train_and_return() -> RandomForestClassifier:
    """Train model with data an return model"""
    data = load_data()
    train, target = prepare_train_data(data)

    return train_model(train, target)


# TODO: Continue here, add functions to execute missing actions
