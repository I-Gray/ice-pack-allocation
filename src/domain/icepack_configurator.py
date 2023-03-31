import logging
from dataclasses import dataclass
from typing import List, Optional

from domain import constants
from domain.exceptions import PostCodeNotFoundException
from domain.models import Box, IceTemperatureRanges, BoxAssignedIce


@dataclass
class IcePackConfigurator:
    boxes: List[Box]
    temperature_ranges: List[IceTemperatureRanges]
    get_temp: callable
    skipped_boxes: Optional[List[Box]] = None

    def pack_boxes_with_ices(self) -> List[BoxAssignedIce]:
        logging.info('configuring ices...')
        boxes_with_ice = []
        for box in self.boxes:
            try:
                temperature = self.get_temp(box.postcode, box.delivery_date)
                boxes_with_ice.append(
                    assign_ice_packs_to_order(box, self.temperature_ranges, temperature)
                )
            except PostCodeNotFoundException as e:
                logging.info(f'{e.postcode} could not be fetched. Skipping box with ID {box.box_id}')
                self.skipped_boxes.append(box)
                continue

        if self.skipped_boxes is not None:
            logging.info('the following boxes were skipped:')
            for skipped_box in self.skipped_boxes:
                logging.info(
                    f"box_id = {skipped_box.box_id}, "
                    f"delivery_date = {skipped_box.delivery_date}"
                )

        logging.info('ices configured!')
        return boxes_with_ice


def assign_ice_packs_to_order(
    box: Box, ice_temp_ranges: List[IceTemperatureRanges], temperature: int
) -> BoxAssignedIce:
    """
    This function attempts to assign the number of ices to a customer
    box uses the ranges, however if the temperature exceeds any of the
    ranges, the constant values are used. (from constants.py)

    :param box: customer box as defined in the models
    :param ice_temp_ranges: the associated number of ices for a given temperature & cool pouch size
    :param temperature: the avg. temperature of the box's delivery date.
    :return: returns a new object with the ice-numbers attached
    """
    num_of_ices = None
    for ice_temp_range in ice_temp_ranges:
        num_of_ices = get_ice_number(box.box_size, temperature, ice_temp_range)
        if num_of_ices is not None:
            return BoxAssignedIce(
                box_id=box.box_id,
                cool_pouch_size=box.cool_pouch_size,
                number_of_ices=num_of_ices,
            )

    if not num_of_ices:
        num_of_ices = get_ices_when_not_in_range(temperature, ice_temp_ranges)
        return BoxAssignedIce(
            box_id=box.box_id,
            cool_pouch_size=box.cool_pouch_size,
            number_of_ices=num_of_ices,
        )


def get_ice_number(
    size: str, temperature: float, ice_range: IceTemperatureRanges
) -> Optional[int]:
    if ice_range.temp_min <= temperature < ice_range.temp_max:
        match size:
            case "S":
                return ice_range.small
            case "M":
                return ice_range.medium
            case "L":
                return ice_range.large
    else:
        return


def get_ices_when_not_in_range(
    temperature: int, ice_temp_ranges: List[IceTemperatureRanges]
) -> int:
    min_temp = min(ice_temp_ranges, key=lambda x: x.temp_min).temp_min
    max_temp = max(ice_temp_ranges, key=lambda x: x.temp_max).temp_max

    if temperature < min_temp:
        logging.info(
            f"Temp value less than lowest explicit ranges. "
            f"Setting ices to the defined min value of - "
            f"{constants.MIN_NUM_ICES}"
        )
        return constants.MIN_NUM_ICES

    elif temperature >= max_temp:
        logging.info(
            f"Temp value exceeded explicit ranges. "
            f"Setting ices to the defined max value of - "
            f"{constants.MAX_NUM_ICES}"
        )
        return constants.MAX_NUM_ICES
