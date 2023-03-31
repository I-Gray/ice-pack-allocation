import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

import requests

from domain.exceptions import PostCodeNotFoundException


@dataclass
class WeatherService:
    api_key: str

    def get_daily_temperature_avg(self, postcode: str, delivery_date: datetime) -> float:
        """
        Gets predicted daily temperature avg. given a delivery date & postcode
        :param api_key: the key needed to access the temperature avg. api
        :api-docs https://dev.meteostat.net/api/
        :param postcode: the delivery postcode of the customers order
        :param delivery_date: the date the order is planned to be delivered
        :return: avg_daily_temp: the average temperature for the postcode on the delivery_date
        """
        lat, lon = get_lat_long_from_postcode(postcode)

        delivery_date_str = delivery_date.strftime("%Y-%m-%d")
        query_params = {
            "lat": lat,
            "lon": lon,
            "start": delivery_date_str,
            "end": delivery_date_str,
        }

        try:
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "meteostat.p.rapidapi.com",
            }

            response = requests.get(
                "https://meteostat.p.rapidapi.com/point/daily",
                headers=headers,
                params=query_params,
            )
            if response.status_code != 200 and (lat or lon) is not None:
                logging.error(f"err: error fetching weather data - {response.text}")
                raise Exception
            elif (lat or lon) is None:
                # Note: for some postcodes the postcode api returns None.
                # for this POC, I set the temp to 25.
                logging.debug('Unable to get weather data - setting temp to 25')
                return 25

            json_rsp = response.json()
            return json_rsp["data"][0]["tavg"]

        except Exception as e:
            logging.error(
                f"err: exception occurred when attempting to get weather information for the following query params - "
                f"{query_params}"
            )
            raise e


def get_lat_long_from_postcode(postcode: str) -> Tuple[float, float]:
    """
    Returns an approx. latitude and longitude values for a UK postcode.
    :api docs: https://postcodes.io/docs
    :param postcode: the postcode to fetch latitude & longitude
    :return: the latitude and longitude as a tuple (can be negative)
    """
    try:
        logging.debug(f"fetching latitude & longitude for postcode - {postcode}")
        response = requests.get("https://api.postcodes.io/postcodes/" + postcode)
        if response.status_code == 404:
            logging.error(f"err: not found - {response.text}")
            raise PostCodeNotFoundException(postcode)
        if response.status_code != 200:
            logging.error(f"err: response not OK - {response.text}")
            raise Exception

        rsp = response.json()
        return rsp["result"]["latitude"], rsp["result"]["longitude"]

    except Exception as e:
        logging.error(
            f"err: exception occurred when attempting to get and return latitude and longitude for postcode - "
            f"{postcode}"
        )
        raise e
