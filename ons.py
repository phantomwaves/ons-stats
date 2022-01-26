import requests
import json
import logging
import pandas as pd
import numpy as np
from pprint import pprint


pd.set_option("max_colwidth", 200)

API_URL = "https://api.beta.ons.gov.uk/v1"


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = '%(asctime)s | %(levelname)8s | %(message)s'

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(logging.Formatter(fmt))
logger.addHandler(stdout_handler)


def get_available_datasets():
    """
    Return a pandas dataframe of available datasets from the ONS API.
    """

    columns = set()

    limit = 1000

    # get datasets json
    r = requests.get(f"{API_URL}/datasets?limit={limit}").json()

    # Get unique column names
    for i in r["items"]:
        for key in i.keys():
            columns.add(key)

    df = pd.DataFrame(r["items"], columns=columns)

    # remove redundant columns
    columns_to_remove = ["license", "keywords", "related_datasets", "national_statistic", "unit_of_measure", "state", "release_frequency"]
    columns_to_rename = {"type":"filterable"}

    df = df.drop(columns_to_remove, axis=1)
    df = df.rename(columns_to_rename, axis=1)

    # clean data
    df["filterable"].fillna(False, inplace=True)
    df["filterable"].replace("filterable", True, inplace=True)

    # return pandas dataframe object
    return df


def get_dataset(datasets, title):
    dataset = datasets.loc[datasets["title"].str.contains(title, case=False, regex=False)]
    
    if dataset.shape[0] > 1:
        logger.info(f"{dataset.shape[0]} datasets found.")
        print(f'{dataset["title"]}')
        choice = int(input("Choose index of desired dataset: "))
        return dataset.loc[choice]

    return dataset


def get_latest_version(dataset):
    links = dict(dataset["links"][8])
    url = links["latest_version"]["href"]

    return url


def get_dataset_dimensions(url):
    dimensions = {}
    r = requests.get(f"{url}/dimensions").json()

    for dimension in r["items"]:
        dimension_label = dimension["label"]
        dimension_id = dimension["links"]["options"]["id"]

        options_url = f"{url}/dimensions/{dimension_id}/options"
        r_2 = requests.get(options_url).json()

        options = {option["label"]: option["option"] for option in r_2["items"]}
        dimensions[dimension_label] = options
    return dimensions
                                                                                                                                                                                                                                                      



if __name__ == "__main__":
    
    datasets = get_available_datasets()

    dataset = get_dataset(datasets, "traffic")

    latest_url = get_latest_version(dataset)

    print(get_dataset_dimensions(latest_url))
