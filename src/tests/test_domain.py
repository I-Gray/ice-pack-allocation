import logging
from unittest.mock import Mock

import pytest

from domain import constants
from domain.data_handle import get_boxes, get_temp_ranges
from domain.icepack_configurator import assign_ice_packs_to_order, IcePackConfigurator
from utils import write_csv


@pytest.mark.parametrize(
    "temperature, expected_ices",
    [
        (-9, 1),
        (4, 2),
        (-10, 1),
        (10, constants.MAX_NUM_ICES),
        (-11, constants.MIN_NUM_ICES),
        (11, constants.MAX_NUM_ICES),
    ],
)
def test_assign_ice_packs_to_order(
    mock_valid_boxes_data, mock_valid_temp_range_data, temperature, expected_ices
):
    actual_box_assigned_ice = assign_ice_packs_to_order(
        mock_valid_boxes_data[1], mock_valid_temp_range_data, temperature=temperature
    )
    assert actual_box_assigned_ice.number_of_ices == expected_ices


def test_icepack_config(mock_valid_boxes_data, mock_valid_temp_range_data):
    get_temp_mock = Mock()
    get_temp_mock.side_effect = [-20, 5, 40]
    ipc = IcePackConfigurator(
        boxes=mock_valid_boxes_data,
        temperature_ranges=mock_valid_temp_range_data,
        get_temp=get_temp_mock
    )
    boxes_with_ice = ipc.pack_boxes_with_ices()
    assert boxes_with_ice[0].number_of_ices == 1
    assert boxes_with_ice[1].number_of_ices == 2
    assert boxes_with_ice[2].number_of_ices == constants.MAX_NUM_ICES


def test_read_boxes_csv(mock_valid_boxes_raw_data):
    with open("test.csv", "w") as f:
        f.write(mock_valid_boxes_raw_data)
    boxes = get_boxes("test.csv")
    assert boxes[0].box_id == 'GB231'
    assert boxes[0].cool_pouch_size == 'M'
    assert boxes[0].box_size == 'L'
    assert boxes[0].postcode == 'CH624SX'


def test_read_temp_range_csv(mock_valid_temp_range_raw_data):
    with open("test.csv", "w") as f:
        f.write(mock_valid_temp_range_raw_data)
    temp_ranges = get_temp_ranges("test.csv")
    assert temp_ranges[0].temp_min == -10
    assert temp_ranges[0].temp_max == 4
    assert temp_ranges[0].small == 1
    assert temp_ranges[0].medium == 1
    assert temp_ranges[0].large == 1


def test_write_csv_success(mock_box_assigned_ice_data):
    file_path = "test.csv"
    write_csv(file_path, mock_box_assigned_ice_data)
    with open(file_path, "r") as f:
        actual_boxes = f.read()

    expected_header = "box_id,cool_pouch_size,number_of_ices\n"
    expected_data = "ID1,M,2\nID2,L,4\n"
    assert actual_boxes == expected_header + expected_data


def test_write_csv_no_data(caplog):
    file_path = "tmp.test.csv"
    data = []

    with caplog.at_level(logging.INFO):
        write_csv(file_path, data)

    assert "no data to write to csv output path " in caplog.text
