import configparser
import json
import logging
from typing import List, Type, TypeVar, cast

import pandas as pd

T = TypeVar("T")


def log_output_file_head(output_filepath: str) -> None:
    df = pd.read_csv(output_filepath)
    logging.info(f"""
        \n
        output file head - located at {output_filepath} :
        \n
        {df.head()}
    """)


def read_csv(
    file_path: str, dataclass: Type[T], mapping: dict, parse_dates=None
) -> List[T]:
    """
    Generic read_csv class that validates the data on the dataclass schema
    :param file_path: filepath to read from (must include '.csv')
    :param dataclass: python dataclass from dataclasses pkg
    :param mapping: mapping between the CSV columns in the file and the dataclass attributes
    :param parse_dates: identifies which columns should be parsed as type DateTime
    :return: a list of objects of the same type as the dataclass defined
    """
    if parse_dates is None:
        parse_dates = []
    try:
        logging.info(f"reading csv file from - {file_path}")
        df = pd.read_csv(file_path, parse_dates=parse_dates)
        df.rename(columns=mapping, inplace=True)
        instances = []
        for row in df.to_dict(orient="records"):
            instance = dataclass(**{k: cast(dataclass, v) for k, v in row.items()})
            instances.append(instance)
        logging.info("csv read successfully")
        return instances

    except (PermissionError, FileNotFoundError, ValueError) as e:
        logging.error(f"err: failed to write csv to filename - {file_path}. - {e}")


def write_csv(file_path: str, data: List[T]) -> None:
    """
    Generic CSV writer that is created based on dataclass object
    :param file_path: filepath to save file (must include '.csv')
    :param data: the list of structured data to write (u
    :return: None
    """
    if not data:
        logging.info(f"no data to write to csv output path {file_path}")
        return

    try:
        logging.info(f"writing csv file to - {file_path}")
        df = pd.DataFrame([vars(d) for d in data])
        df.to_csv(file_path, index=False)
        logging.info("csv written successfully")

    except (PermissionError, FileNotFoundError, ValueError) as e:
        logging.error(f"err: failed to read csv to filepath - {file_path}. - {e}")
