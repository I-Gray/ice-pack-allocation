import textwrap
from datetime import datetime
from typing import List
from unittest.mock import MagicMock

import pytest
from datetime import datetime

from domain.models import Box, IceTemperatureRanges, BoxAssignedIce


@pytest.fixture
def mock_valid_boxes_raw_data() -> str:
    return """box_id,delivery_date,Cool Pouch Size,Box Size,postcode
GB231,19/02/2022 00:00,M,L,CH624SX
GB1481,20/02/2022 00:00,M,M,LS178RS
GB1681,20/02/2022 00:00,M,M,CO27LR
    """


@pytest.fixture
def mock_valid_temp_range_raw_data() -> str:
    return """temperature_min,temperature_max,S,M,L
-10,4,1,1,1
4,10,1,2,2
    """


@pytest.fixture
def mock_valid_boxes_data() -> List[Box]:
    return [
        Box(
            box_id="GB231",
            delivery_date=datetime.strptime("18/02/2023 00:00", "%d/%m/%Y %H:%M"),
            cool_pouch_size="S",
            box_size="L",
            postcode="CH624SX",
        ),
        Box(
            box_id="GB678",
            delivery_date=datetime.strptime("19/02/2023 00:00", "%d/%m/%Y %H:%M"),
            cool_pouch_size="M",
            box_size="M",
            postcode="TN257GH",
        ),
        Box(
            box_id="GB1481",
            delivery_date=datetime.strptime("20/02/2023 00:00", "%d/%m/%Y %H:%M"),
            cool_pouch_size="L",
            box_size="M",
            postcode="LS178RS",
        ),
    ]


@pytest.fixture
def mock_valid_temp_range_data() -> List[IceTemperatureRanges]:
    return [
        IceTemperatureRanges(
            temp_min=-10,
            temp_max=4,
            small=1,
            medium=1,
            large=1,
        ),
        IceTemperatureRanges(
            temp_min=4,
            temp_max=10,
            small=1,
            medium=2,
            large=2,
        ),
    ]


@pytest.fixture
def mock_box_assigned_ice_data() -> List[BoxAssignedIce]:
    return [
        BoxAssignedIce(
            box_id='ID1',
            cool_pouch_size='M',
            number_of_ices=2
        ),
        BoxAssignedIce(
            box_id='ID2',
            cool_pouch_size='L',
            number_of_ices=4
        ),
    ]


@pytest.fixture
def mock_postcode_response():
    response_mock = MagicMock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        "result": {
            "latitude": 12.1,
            "longitude": 13.2
        }
    }
    return response_mock


@pytest.fixture()
def mock_weather_response():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "data": [
            {
                "tavg": 10.0
            }
        ]
    }
    return response

