import requests
import json
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

API_URL = "https://api.beta.ons.gov.uk/v1"


def get_available_datasets():
    """
    Return a list of available datasets from the ONS API.
    """

    columns = set()
    limit = 1000

    r = requests.get(f"{API_URL}/datasets?limit={limit}").json()

    for i in r["items"]:
        for key in i.keys():
            columns.add(key)

    df = pd.DataFrame(r["items"], columns=columns)

    columns_to_remove = ["license", "keywords", "related_datasets", "national_statistic", "unit_of_measure", "state", "release_frequency"]
    columns_to_rename = {"type":"filterable"}

    df = df.drop(columns_to_remove, axis=1)
    df = df.rename(columns_to_rename, axis=1)

    df["filterable"].fillna(False, inplace=True)
    df["filterable"].replace("filterable", True, inplace=True)


    return df

data = get_available_datasets()
