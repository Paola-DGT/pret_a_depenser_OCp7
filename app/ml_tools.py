"""This module contains all that is needed to preform model tasks."""
import logging
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

logger = logging.getLogger("ml-tools")


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Reads the base features working file"""
    try:
        train = pd.read_csv("app/data/train.csv")
        labels = pd.read_csv("app/data/labels.csv")
        return train, labels
    except FileNotFoundError as error:
        logger.error("Cannot read features file, ERROR %s: ", error)
        raise


def prepare_train_data(train: pd.DataFrame) -> pd.DataFrame:
    """Prepares data for training the model."""
    train.drop(["SK_ID_CURR"], axis=1, inplace=True)

    imp = SimpleImputer(missing_values=np.nan, strategy="median")
    imp.set_output(transform="pandas")
    train = imp.fit_transform(train)

    return train


def prepare_predict_data(data: dict) -> dict:
    """Prepares the input dict to be used in prediction"""
    # TODO: The input dictionary will contain unecessary columns that have to be
    #   stripped away to be able to use it. Add the dictionary cleanin here and
    #   return a clean dictionary.
    return data


def train_model(data: pd.DataFrame, target: pd.DataFrame) -> RandomForestClassifier:
    """Trains a random forest model and returns it for further operations"""
    random_forest = RandomForestClassifier(n_estimators=5, random_state=150, n_jobs=-1)
    random_forest.fit(data, target)

    return random_forest


def append_new_customer():
    """Appends the new customer to the existing dataset.
    The dictionary must have all the columns of the dataset.
    """
    # TODO: Add logic to append customer


def train_and_return() -> RandomForestClassifier:
    """Train model with data an return model"""
    train, target = load_data()
    train = prepare_train_data(train)

    return train_model(train, target)


# TODO: Continue here, add functions to execute missing actions
