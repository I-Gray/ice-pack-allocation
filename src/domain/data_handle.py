import logging
from typing import List, Tuple

from domain.models import IceTemperatureRanges, Box
from utils import read_csv


def import_data(data_filepath: str) -> Tuple[List[Box], List[IceTemperatureRanges]]:
    logging.info("Importing data")

    box_filename = "Boxes.csv"
    boxes = get_boxes(data_filepath + box_filename)

    temp_filename = "Temperature_bands.csv"
    temperature_ranges = get_temp_ranges(data_filepath + temp_filename)

    return boxes, temperature_ranges


def get_temp_ranges(data_filepath) -> List[IceTemperatureRanges]:
    temp_headers = {
        "temperature_min": "temp_min",
        "temperature_max": "temp_max",
        "S": "small",
        "M": "medium",
        "L": "large",
    }
    temperature_ranges = read_csv(data_filepath, IceTemperatureRanges, temp_headers)
    return temperature_ranges


def get_boxes(data_filepath) -> List[Box]:
    box_headers = {
        "box_id": "box_id",
        "delivery_date": "delivery_date",
        "Cool Pouch Size": "cool_pouch_size",
        "Box Size": "box_size",
        "postcode": "postcode",
    }
    date_columns = ["delivery_date"]
    boxes = read_csv(data_filepath, Box, box_headers, date_columns)
    return boxes
